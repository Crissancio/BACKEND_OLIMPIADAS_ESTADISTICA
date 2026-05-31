import logging

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.scheduler.jobs.email_jobs import finalize_campaigns, process_scheduled_campaigns, send_pending_emails
from app.scheduler.jobs.temp_jobs import cleanup_temp_directory

logger = logging.getLogger(__name__)

jobstores = {"default": MemoryJobStore()}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone=settings.scheduler_timezone)
_listener_registered = False


def listener_errores_scheduler(event):
    if event.exception:
        logger.error("El job %s fallo de forma critica: %s", event.job_id, event.exception, exc_info=True)
    else:
        logger.debug("Job %s ejecutado correctamente.", event.job_id)


def configure_scheduler_jobs():
    global _listener_registered

    if not _listener_registered:
        scheduler.add_listener(listener_errores_scheduler, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        _listener_registered = True

    scheduler.add_job(
        process_scheduled_campaigns,
        "interval",
        minutes=1,
        id="process_campaigns",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.add_job(
        send_pending_emails,
        "interval",
        minutes=settings.mailing_interval_minutes,
        id="send_emails",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.add_job(
        finalize_campaigns,
        "interval",
        minutes=2,
        id="finalize_campaigns",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.add_job(
        cleanup_temp_directory,
        "interval",
        hours=settings.temp_cleanup_interval_hours,
        id="cleanup_temp",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )


def start_scheduler():
    if not settings.scheduler_enabled:
        logger.warning("APScheduler esta desactivado en las variables de entorno.")
        return

    if scheduler.running:
        logger.info("APScheduler ya estaba corriendo.")
        return

    configure_scheduler_jobs()
    scheduler.start()
    logger.info("APScheduler corriendo en segundo plano.")


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler detenido.")

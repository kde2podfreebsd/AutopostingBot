from datetime import datetime

from Bot.Config import bot
from DataBase.DataAccessLayer.ChainDAL import ChainDAL
from DataBase.session import async_session


class ScheduledTasks:

    _instance = None

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.existing_jobs = {}

    async def process_chain(self):
        await bot.send_message(406149871, "execute task at time")

    async def schedule_chains(self):
        async with async_session() as session:
            chain_dal = ChainDAL(session)
            active_chains = await chain_dal.getActiveChains()

            if len(active_chains) == 0:
                print("No tasks to execute")
            else:
                for chain in active_chains:
                    chain_id = chain[0].chain_id
                    chain_parsing_times = chain[0].parsing_time

                    if self.existing_jobs.get(chain_id) is None:
                        self.existing_jobs[chain_id] = {
                            "chain_id": chain_id,
                            "chain_times": chain_parsing_times,
                            "is_added": False,
                            "jobs": [],
                        }

                        for parsing_time in chain_parsing_times:
                            scheduled_time = datetime.strptime(parsing_time, "%H:%M").time()
                            job = self.scheduler.add_job(
                                self.process_chain,
                                "cron",
                                hour=scheduled_time.hour,
                                minute=scheduled_time.minute,
                            )
                            jobs_list = self.existing_jobs[chain_id]["jobs"]
                            jobs_list.append(job)
                            self.existing_jobs[chain_id]["jobs"] = jobs_list
                            self.existing_jobs[chain_id]["is_added"] = True

                    if (
                        self.existing_jobs[chain_id]["is_added"]
                        and chain_parsing_times
                        == self.existing_jobs[chain_id]["chain_times"]
                    ):
                        continue

                    if (
                        self.existing_jobs[chain_id]["is_added"]
                        and chain_parsing_times
                        != self.existing_jobs[chain_id]["chain_times"]
                    ):
                        for job in self.existing_jobs[chain_id]["jobs"]:
                            job.remove()

                        self.existing_jobs[chain_id]["jobs"] = []
                        self.existing_jobs[chain_id]["chain_times"] = chain_parsing_times

                        for parsing_time in chain_parsing_times:
                            scheduled_time = datetime.strptime(parsing_time, "%H:%M").time()
                            job = self.scheduler.add_job(
                                self.process_chain,
                                "cron",
                                hour=scheduled_time.hour,
                                minute=scheduled_time.minute,
                            )
                            jobs_list = self.existing_jobs[chain_id]["jobs"]
                            jobs_list.append(job)
                            self.existing_jobs[chain_id]["jobs"] = jobs_list
                            self.existing_jobs[chain_id]["is_added"] = True

    def run(self):
        self.scheduler.add_job(
            self.schedule_chains, "interval", seconds=5
        )
        self.scheduler.start()
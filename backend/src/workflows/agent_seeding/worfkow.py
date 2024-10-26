from temporalio import workflow


@workflow.defn
class AgentSeedingWorkflow:
    @workflow.run
    async def run(self, input: AgentSeedingInput) -> None:
        pass
        # Fetch all seeds for the agent
        # for each seed, -> seed the agent

from cognite.seismic._api.api import API
from cognite.seismic.protos.ingest_service_messages_pb2 import StatusRequest


class JobAPI(API):
    def __init__(self, ingestion, metadata):
        super().__init__(metadata=metadata, ingestion=ingestion)

    def status(self, job_id: str = None):
        """Get the status of an ingestion job

        Args:
            job_id (str): The id of the job

        Returns:
            The status of the job, including latest step performed
        """
        request = StatusRequest(job_id=job_id)
        return self.ingestion.Status(request=request, metadata=self.metadata)

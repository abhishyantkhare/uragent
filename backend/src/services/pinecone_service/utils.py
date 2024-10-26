from pinecone.exceptions import ServiceException


def already_exists_error(e: ServiceException):
    print("RETRYING")
    return e.status == "AlreadyExists"

from havenondemand.hodclient import *

client = HODClient("5dd151bb-5a5c-4514-8528-141a46e7cd53", version="v2")

api_key = 'e1a2805e-db2e-431e-bc93-b55aca246795'


def speech_to_text(audio_url):
    """
    Перевести аудиофайл в текст.
    :param audio_url: url на аудиофайл с русской речью
    :return: распознанный текст
    """
    params = {'url': audio_url, 'language': 'ru-RU'}
    response_async = client.post_request(params, HODApps.RECOGNIZE_SPEECH,
                                         async=True)
    jobID = response_async['jobID']
    response = client.get_job_status(jobID)
    print(response_async)

    while response['actions'][0]['status'] != 'finished':
        response = client.get_job_status(jobID)
        print(response)
        time.sleep(2)

    return response['actions'][0]['result']['document'][0]['content']

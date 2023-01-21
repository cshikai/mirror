import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import streamlit as st
import json
from typing import List, Tuple, ByteString

class Uploader:
    def __init__(self, config: dict) -> None:
        self.batch_size = config['ui_service']['batch_size']
        self.url = f"http://{config['gateway']['host']}:{config['gateway']['port']}/upload"
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def format_data(self, entry: ByteString, source: str) -> dict:
        entry = entry.decode('utf8').strip()[:-1]
        entry = json.loads(entry)
        entry['doc_id'] = entry.pop('_id')
        entry['doc_timestamp'] = self.timestamp
        entry['source'] = source
        entry["medium"] =  "text"
        entry['content'] = entry.pop('text')
        entry['content_type'] = 'text'
        entry.pop('metadata', None)
        return entry

    def process(self, entries: List[dict], batch_index: int) -> Tuple[int, requests.models.Response]:
        response = requests.post(self.url, json = {'data': entries})
        return (batch_index, response)

    def upload_file(self, executer: ThreadPoolExecutor, file: st.runtime.uploaded_file_manager.UploadedFile) -> List[Tuple[int, requests.models.Response]]:
        results = []
        temp = []
        batch_idx = 0
        futures = []
        for entry in file:
            entry = self.format_data(entry, file.name)
            temp.append(entry)
            if len(temp) == self.batch_size :
                batch_idx += 1
                futures.append(executer.submit(self.process, temp, batch_idx))
                temp = []
        if len(temp) > 0:
            batch_idx += 1
            futures.append(executer.submit(self.process, temp, batch_idx))
            temp = []

        for future in as_completed(futures):
            results.append(future.result())

        results.sort(key=lambda x: x[0])
        return results

    def check_results(self,upload_results: dict) -> None:
        for key, results in upload_results.items():
            if len(results) <= 0:
                raise Exception('Incomplete')
            for response in results:
                if response[1].status_code != 200:
                    raise Exception('Some/All batch failed')

    def upload_all(self, list_files: List[st.runtime.uploaded_file_manager.UploadedFile]) -> None:
        upload_results = {}
        with ThreadPoolExecutor() as executer:
            for file in list_files:
                upload_results[file.name] = self.upload_file(executer, file)
        try:
            self.check_results(upload_results)
            st.success("Upload success!")
        except Exception as e:
            st.warning(f'Incomplete upload: {upload_results}', icon="⚠️")
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import sys
import argparse
import os
from tqdm import tqdm

class ScrapeYoutube():
    def __init__(self, input, output):
        self.url = input
        self.output = output
        self.youtube_list = self.read_video_list()
        self.output_meta = {}

        self.extract_video_meta()
        self.export_video_meta()

    def read_video_list(self):
        youtube_list = pd.read_csv(self.url)
        return youtube_list['url']

    def extract_video_meta(self):
        print('Initializing video extraction')

        for idx, source in enumerate(tqdm(self.youtube_list)):
            source_text = requests.get(source).text
            soup = BeautifulSoup(source_text, 'lxml')
            div_s = soup.findAll('div')


            title = div_s[1].find('span', class_='watch-title')
            if title:
                title = title.text.strip()

            vid = {'title': title, 'link':source}
            self.output_meta[idx] = vid

        print(f'Metadata extractions completed for {len(self.youtube_list)} videos')
            
    def export_video_meta(self):
        output_path = os.path.join(self.output, 'metadata.json')

        print(f'Exporting extracted metadata to {output_path}')

        with open(output_path, 'w') as f:
            json.dump(self.output_meta, f)

        print('Finished exporting...')

if __name__ == '__main__':      
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Path to your csv containing urls to youtube videos', required=True)
    parser.add_argument('--output', help='Path to the extracted metadata json output', required=True)
    args = parser.parse_args()
    Youtube = ScrapeYoutube(args.input, args.output)
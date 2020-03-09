import os
import sys
import json
import argparse
import requests

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils.class_selector import *

class ScrapeYoutube():
    def __init__(self, input_file, output_dir):
        self.youtube_list = self.read_video_list(input_file)
        self.output_meta = {}

        self.extract_video_meta()
        self.export_video_meta(output_dir)

    def read_video_list(self, input_file):
        """Read list of video urls in a csv format given 'url' as the file header
        
        Arguments:
        - 'input_file': csv file with 'url' as the file header
        """
        youtube_list = pd.read_csv(input_file)
        return youtube_list['url']

    def extract_video_meta(self):
        """
        Extract the following information:
        1) Title (str)
        2) View Count (int)
        3) Likes (int)
        4) Dislikes (int)
        """
        print('Initializing video extraction')

        def strip_whitespace(content):
            """ Strip trailing and leading characters if content is not null/undefined
        
            Arguments:
            - 'content': string to be stripped
            """
            if content:
                content = content.text.strip()
            return content

        for idx, source in enumerate(tqdm(self.youtube_list)):
            source_text = requests.get(source).text
            soup = BeautifulSoup(source_text, 'lxml')
            div_s = soup.findAll('div')

            # Extracting title
            title = div_s[1].find('span', class_ = TITLE_CLASS)
            title = strip_whitespace(title)
            
            # Extracting view count
            view_count = div_s[1].find(class_= VIEWS_CLASS)
            view_count = int(strip_whitespace(view_count).split(' ')[0].replace(',', ''))
            
            # Extracting likes
            likes = div_s[1].find('button', class_ = LIKES_CLASS)
            likes = int(strip_whitespace(likes))

            # Extracting dislikes
            dislikes = div_s[1].find('button', class_= DISLIKES_CLASS )
            dislikes = int(strip_whitespace(dislikes))

            # Aggregating metadata
            vid_object = {
                    'title': title, 
                    'source': source, 
                    'view_count': view_count,
                    'likes' : likes,
                    'dislikes' : dislikes
            }
            self.output_meta[idx] = vid_object

        print(f'Metadata extractions completed for {len(self.youtube_list)} videos')
            
    def export_video_meta(self, output_dir):
        """Export the video metadata into JSON file in the file specified
        
        Arguments:
        - 'output_dir': the directory for the output JSON file
        """

        output_path = os.path.join(output_dir, 'metadata.json')

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
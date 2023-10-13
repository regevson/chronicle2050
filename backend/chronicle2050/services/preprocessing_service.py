# preprocessing-service

import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def split_into_sentences(articles):
    sentences = []
    timestamps = []
    links = []
    for idx, row in articles.iterrows():
        article = row['excerpt']
        timestamp = row['published_date']
        link = row['link']
        # tokenize content into sentences
        for sentence in sent_tokenize(article):
            sentences.append(sentence)
            timestamps.append(timestamp)
            links.append(link)

    # create new dataframe with each sentence and its corresponding timestamp
    sentences_df = pd.DataFrame({
        'sentence': sentences,
        'timestamp': timestamps,
        'link': links
    })
    sentences_df.dropna(subset=['sentence'], inplace=True)
    return sentences_df

def analyze_sentence_length(sentences):
    sentences['len'] = sentences['sentence'].apply(len)
    return sentences[sentences['len'] >= 30]

def drop_duplicate_links(articles):
    #print(articles.duplicated(subset=['link'], keep=False).sum())
    articles.drop_duplicates(subset='link', keep='first', inplace=True) # duplicate articles from the same source are useless

def drop_duplicates(sentences):
    sentences['num_duplicates'] = sentences.groupby('sentence')['sentence'].transform('count')
    return sentences.drop_duplicates(subset='sentence', keep='first')

'''
def drop_duplicates(sentences):
    sentences['num_duplicates'] = sentences.groupby('sentence')['sentence'].transform('count')
    aggregated_sources = sentences.groupby('sentence')['link'].agg(list).reset_index()
    aggregated_sources.rename(columns={'link': 'links'}, inplace=True)
    sentences.drop_duplicates(subset='sentence', keep='first', inplace=True)
    sentences = pd.merge(sentences, aggregated_sources, on='sentence')
    sentences['links'] = sentences['links'].apply(lambda x: ','.join(x))
    return sentences
'''

def resolve_newline(sentences):
    def resolve(sentence):
        return sentence.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    sentences['sentence'] = sentences['sentence'].apply(resolve)

def preprocess_news(articles):
    drop_duplicate_links(articles)
    sentences = split_into_sentences(articles)
    sentences = analyze_sentence_length(sentences)
    sentences = drop_duplicates(sentences)
    resolve_newline(sentences)
    return sentences

def prepare_data_for_frontend(sentences):
    stats = {'numSentsWithDate': sentences[sentences['datetime'] == ''].shape[0],
             'numSentsWithoutDate': sentences[sentences['datetime'] != ''].shape[0],
             'numClusters': len(sentences['cluster_id'].unique())}
    topic_groups = sentences.groupby('cluster_id') # make new dataframe (group) for every topic (cluster)
    topics = []
    for cluster_id, topic_group in topic_groups:
        json_obj = {'clusterID': cluster_id, 'keywords': topic_group.iloc[0]['keywords']}
        avg_mentions = topic_group['mentions'].sum()/len(topic_group)
        json_obj['avgTotalMentions'] = float(avg_mentions)

        date_groups = topic_group.groupby('datetime')
        content_with_date = []
        content_without_date = []
        for date, date_group in date_groups:
            content = {}

            sents = []
            for row_id, row in date_group.iterrows():
                sent = {'sentence': row['sentence'],
                        'mentions': row['mentions'],
                        'link': row['link'],
                        'links': row['links'],
                        'timestamp': row['timestamp'],
                       }
                sents.append(sent)

            sum_of_mentions = date_group['mentions'].sum()
            #sum_of_mentions = len(date_group)
            content['sumOfMentions'] = float(sum_of_mentions)

            if date:
                content['datetime'] = str(row['datetime'])
                content_with_date.append(content)
            else:
                content_without_date.append(content)

            content['sentences'] = sents

        json_obj['contentWithDate'] = content_with_date
        json_obj['contentWithoutDate'] = content_without_date
        topics.append(json_obj)

    return {'stats': stats, 'data': topics}

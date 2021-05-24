from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import pandas

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    calendar = service.calendarList().list().execute()
    calendar_list = calendar['items']

    fig = go.Figure()
    for i in calendar_list:
        if i['id'] == 'makccom0@gmail.com':
            continue
        if i['id'] == 'ru.russian#holiday@group.v.calendar.google.com':
            continue
        date_list = []
        summ_events_day = {}
        events = service.events().list(calendarId=i['id']).execute()
        for j in events['items']:
            try:
                date = j['start']['dateTime'].split('T')[0]
            except:
                try:
                    date = j['start']['date'].split('T')[0]
                except:
                    continue

            if date not in summ_events_day:
                summ_events_day[date] = 1
            else:
                summ_events_day[date] += 1


        list_summ = []
        for j in sorted(summ_events_day.keys()):
            list_summ.append(summ_events_day[j])
            date_list.append(j)

        fig.add_trace(go.Scatter(x=date_list, y=list_summ, mode='lines+markers', line_shape='linear', hovertemplate='Дата: %{x}<br>Просмотров: %{y}'))


    fig.show()
if __name__ == '__main__':
    main()
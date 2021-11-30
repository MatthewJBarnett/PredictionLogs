import datetime, json, os, time
from metaculus_login import main_session, pandemic_session

# This script updates info for open, closed, and resolved questions.
# It also updates the list of open questions on the pandemic subdomain.

filename = 'questions.json'
pandemic_filename = 'pandemic_questions.json'

date = datetime.datetime.utcnow().isoformat()
questions = {'results': {}, 'date': ''}
pandemic_qs = {'results': {}, 'date': ''}

# Load previous data, if it exists
if os.path.isfile(filename):
  with open(filename, 'r') as file:
    questions = json.load(file)

if os.path.isfile(pandemic_filename):
  with open(pandemic_filename, 'r') as file:
    pandemic_qs = json.load(file)

# status is one of {open, closed, resolved}
# order_by is the column to order API results by
def fetch_results(status, order_by, date, site='www.metaculus.com'):
  global main_session, pandemic_session
  s = main_session if 'www' in site else pandemic_session
  results = {}
  i = 1

  while True:
    url = f'https://{site}/api2/questions/?order_by=-{order_by}&status={status}&page={i}'
    print(url)
    data = s.get(url).json()
    time.sleep(1)

    if 'results' not in data:
      return results
    for d in data['results']:
      d['question_status'] = status
      if order_by in d and d[order_by] < date:
        return results
      else:
        results[d['id']] = d
    i += 1

results = {}
results.update(fetch_results('open', 'last_activity_time', questions['date']))

questions['results'].update(results)
questions['date'] = date

with open(filename, 'w') as file:
  json.dump(questions, file)

with open(pandemic_filename, 'w') as file:
  json.dump(pandemic_qs, file)


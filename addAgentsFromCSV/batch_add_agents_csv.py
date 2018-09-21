import urllib
import csv


def main():
    # Validate API KEY
    api_key = raw_input('Hello, please provide your REST API key: ')
    check_api_url = 'https://surfly.com/v2/sessions/'
    check_api_url += '?api_key=' + api_key + '&active_session=true'
    try:
        check_api_response = urllib.urlopen(check_api_url)
    except urllib.error as e:
        print e
        return
    c = check_api_response.code
    x = check_api_response.read()
    if c != 200:
        print c, x
        return
    print 'Your API KEY is valid.'

    # Creates Surfly agent with API call
    def create_agent(agent_name, agent_email, init_password):
        url = 'https://surfly.com/v2/agents/?api_key=' + api_key
        params = urllib.urlencode({'username': agent_name,
                                   'agent_email': agent_email,
                                   'password': init_password})
        try:
            response = urllib.urlopen(url, params)
        except Exception as e:
            print e
        c = response.code
        x = eval(response.read())
        if c == 200:
            agent_id = x['agent_id']
            print c, '\''+agent_name+'\'', 'added successfully. Agent ID: ' \
                     + str(agent_id)
            return {'created': True, 'detail': {'agent_id': agent_id}}
        elif c == 400:
            print c, '\''+agent_name+'\'', x['error']
            return {'created': False, 'detail': x['error']}
        else:
            print c, x

    # ** init_password is technically not an initial password, need to plan how
    # to actually enforce its change upon login? **
    print 'You can now add agents in batch by providing a valid CSV file.'
    print 'Each row should contain the following: ad. Do not include headers.'

    input_csv = raw_input('Please provide a path to your input CSV file: ')
    output_csv = 'surfly_agents_added_report.csv'

    with open(input_csv, 'rb') as input_file:
        reader = csv.reader(input_file)
        with open(output_csv, 'wb') as output_file:
            writer = csv.writer(output_file)

            # Adding header to output_csv file
            writer.writerow(['agent_name',
                             'agent_email',
                             'password',
                             'status',
                             'details'])

            for row in reader:
                try:
                    agent = create_agent(row[0], row[1], row[2])
                except Exception as e:
                    print e
                    continue

                if agent['created'] is True:
                    writer.writerow([row[0], row[1], row[2],
                                    'OK', agent['detail']])

                elif agent['created'] is False:
                    writer.writerow([row[0], row[1], row[2],
                                    'Failed', agent['detail']])

    input_file.close()
    output_file.close()
    print output_csv, 'has been saved to your current directory.'


if __name__ == '__main__':
    # execute only if run as a script
    main()

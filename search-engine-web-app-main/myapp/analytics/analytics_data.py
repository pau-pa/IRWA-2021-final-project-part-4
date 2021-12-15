import json
import random


class AnalyticsData:
    total_visits = 1
    pages_viewed = 1

    pages_visited = {}

    ips = []
    user_agents = {
        'Mozilla/5.0 (X11Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36': 3,
        'Mozilla/5.0 (Windows NT 6.1WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36': 2,
        'Mozilla/5.0 (Windows NT 6.1 WOW64 Trident/7.0 rv: 11.0) like Gecko': 2,
        'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9': 4,
        'Mozilla/5.0 (iPad CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4': 3,
    }

    def add_main_page_visit(self, user):
        self.store_user_data(user)
        self.total_visits += 1

    def page_visited(self, user, tweet_id):
        print(tweet_id)
        if tweet_id in self.pages_visited:
            self.pages_visited[tweet_id]['times'] += 1
            if user.user_agent in self.pages_visited[tweet_id]['user-agent']:
                self.pages_visited[tweet_id]['user-agent'][user.user_agent] += 1
            else:
                self.pages_visited[tweet_id]['user-agent'][user.user_agent] = 1
        else:
            self.pages_visited[tweet_id] = {
                'times': 1,
                'user-agent': {
                    user.user_agent: 1
                }
            }
            self.pages_viewed += 1

    def store_user_data(self, user):
        self.ips.append(user.ip_address)
        if user.user_agent not in self.user_agents:
            self.user_agents[user.user_agent] = 1
        else:
            self.user_agents[user.user_agent] += 1

    def get_user_agent_list(self):
        return list(self.user_agents.keys())

    def get_user_agent_values(self):
        return list(self.user_agents.values())

    def get_num_user_agents(self):
        return len(self.user_agents.keys())

    def get_user_agents_by_id(self, tweet_id):
        return list(self.pages_visited[tweet_id]['user-agent'].keys())

    def get_user_agents_by_id_values(self, tweet_id):
        return list(self.pages_visited[tweet_id]['user-agent'].values())


class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

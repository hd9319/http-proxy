import re
import random
import time
import requests
from urllib.parse import urlparse

class ProxyRequest:
    def __init__(self, proxy_urls_path, user_agents_path, timer=0)
                 acceptable_status_codes=[200]):

        self.rotate_agent = rotate_agent
        self.rotate_proxy = rotate_proxy
        self.acceptable_status_codes = acceptable_status_codes
        self.proxies = []
        self.failed_proxy_sites = []
        self.proxy_tracker = {}
        self.domain_tracker = {}
        self.failed_proxies = []

        if proxy_urls_path:
            with open(proxy_urls_path, 'r') as readfile:
                self.proxy_urls = readfile.readlines()

        if user_agents_path:
            with open(user_agents_path, 'r') as readfile:
                self.user_agents = readfile.readlines()

    def refresh_proxies(self):
        urls = list(set(self.proxy_urls) - set(self.failed_proxy_sites))
        for idx, url in enumerate(urls):
            if idx % 10 == 0:
                print('Retrieved Proxies from: %d/%d pages' % (idx + 1, len(urls)))
            try:
                response = requests.get(url, headers=self.headers)
                _ = _add_proxies(_parse_proxies(response))
            except Exception as e:
                self.failed_proxy_sites.append(url)
            print('Completed Retrieving Proxies.')

    def _parse_proxies(self, response):
        proxies = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', response.text)
        return proxies

    def _add_proxies(self, proxies):
        new_proxies = list(set(proxies) - set(self.proxy_tracker.keys()))
        self.proxies += new_proxies
        self.proxy_tracker.update({proxy:0 for proxy in new_proxies})

    def _track_response(self, response, response_time):
        domnain = urlparse(response.url).netloc
        if domain not in self.domain_tracker:
            _ = self._add_domain(domain)

        if response.status_code in acceptable_status_codes:
            self.domain_tracker[domain]['successes'] += 1
        else:
            self.domain_tracker[domain]['failures'] += 1

        domain_stats = self.domain_tracker[domain]
        self.domain_tracker[domain]['avg_response_time'] = self._calculate_avg_time(domain_stats['avg_response_time'], \
                                                                                   response_time, \
                                                                                   domain_stats['total_requests'])
        self.domain_tracker[domain]['total_requests'] += 1

    def _add_domain(self, domain):
        self.domain_tracker[domain] = {'avg_response_time': 0, 'successes': 0, \
                                      'failures': 0, 'total_requests': 0}

    def _calculate_avg_time(self, current_avg, response_time, total_requests):
        return (current_avg * total_requests + response_time) / total_requests + 1

    def _validate_response(self, response, proxies):
        if response.status_code not in self.acceptable_status_codes and proxies:
            for _, proxy in proxies.items():
                self.proxy_tracker[proxy] += 1
                if self.proxy_tracker[proxy] > self.threshold:
                    self.proxies.remove(proxy)
                    self.failed_proxies.append(proxy)

    def request(self, url, headers, rotate_proxy=True, rotate_agent=True):
        _ = time.sleep(self.timer)
        if rotate_proxy:
            proxy_dict = {'http': random.choice(self.proxies), \
                          'https': random.choice(self.proxies)}

        if headers and rotate_agent:
            headers['User-Agent'] = random.choice(self.user_agents)

        response = requests.get(url, headers=headers, proxies=proxy_dict)
        _ = _validate_response(response)
        return {'response': response, 'proxies': proxy_dict, 'headers': headers}

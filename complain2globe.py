import os
import re
import json
import time
import random
import twitter
import subprocess

"""Monitor: Class that handles the SpeedTest and Twitter Posts"""
class Monitor():

    def __init__(self):
        self.speed = SpeedTest()
        self.config = json.load(open('./config.json'))
        self.twitter = TwitterTat(self.config, self.speed)

    def run(self):
        try:
            self.runSpeedTest()
            if self.speed.getDownSpeed() < self.config['internetCalculatedSpeed'] :
                self.twitter.tweetResult()
        except Exception as e:
            print "Monitor Exception"

    def runSpeedTest(self):
        self.speed.start()

"""SpeedTest: Class that uses speedtest-cli(speedtest.net) and reports back results"""
class SpeedTest():
    """docstring for SpeedTest"""
    def __init__(self):
        self.pingResult = None
        self.downSpeedResult = None
        self.upSpeedResult = None

    def start(self):
        self.doSpeedTest()

    def doSpeedTest(self):

        try:
            result = subprocess.check_output('/usr/local/bin/speedtest-cli')
            self.parseSpeedTest(result)
        except Exception as e:
            print "SpeedTest Exception!"

    def parseSpeedTest(self, result):
        resultArray = result.split('\n')
        self.pingResult = re.findall("\d+\.\d+", resultArray[4])[-1]
        self.downSpeedResult = re.findall("\d+\.\d+", resultArray[6])[-1]
        self.upSpeedResult = re.findall("\d+\.\d+", resultArray[8])[-1]

    def getPing(self):
        return self.pingResult

    def getDownSpeed(self):
        return self.downSpeedResult

    def getUpSpeed(self):
        return self.upSpeedResult

"""TwitterTat: Class that handles all Twitter Posts and mechanisms"""
class TwitterTat():
    """docstring for TwitterTat"""
    def __init__(self, config, speed):
        self.config = config
        self.speed = speed

    def organizeTweet(self):
        return (self.config['tweetThresholds'][random.randrange(0, len(self.config['tweetThresholds']))]).replace('{tweetTo}', self.config['tweetTo']).replace('{internetSpeed}', self.config['internetSpeed']).replace('{downloadResult}', self.speed.getDownSpeed()).replace('{monthlyPayment}', self.config['monthlyPayment'])

    def tweetResult(self):
        try:
            message = self.organizeTweet()
            if message:
                api = twitter.Api(consumer_key=self.config['twitter']['twitterConsumerKey'],
                consumer_secret=self.config['twitter']['twitterConsumerSecret'],
                access_token_key=self.config['twitter']['twitterToken'],
                access_token_secret=self.config['twitter']['twitterTokenSecret'])
                if api:
                    status = api.PostUpdate(message)
        except Exception as e:
            print "TwitterTat Exception"

def main():
    #Put no. of seconds
    while 1:
        try:
            print "--------------------------------------"
            print "|  complain2globe by @dinosaurfiles  |"
            print "|          Start the NOISE!          |"
            print "--------------------------------------"
            monitor = Monitor()
            monitor.run()
            time.sleep(1800)
        except Exception as e:
            print "Main Exception"

if __name__ == '__main__':
    main()

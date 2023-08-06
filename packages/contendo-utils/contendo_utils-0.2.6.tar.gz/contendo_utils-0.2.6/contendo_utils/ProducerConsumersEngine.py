from datetime import datetime as dt, timedelta
import os
import multiprocessing
import time
import pandas as pd

class ProducerConsumersEngine():
    #
    # read in the configurations
    def __init__(self, producerFunc):
        #
        # get the initial configuration
        #self.consumerStatus = multiprocessing.Queue()
        self.sentinel = 'Done'
        self.producerFunc = producerFunc
        self.jobsQueue = multiprocessing.JoinableQueue()  # start a joinable queue to pass messages
        self.handlers = {}

    def register_handler(self, name, func):
        self.handlers[name] = func

    def main_consumer_func(self, i, **kwargs):
        #
        # execute a list of query jobs
        #print('Start executor %d' % i)
        try:
            for jobData in iter(self.jobsQueue.get, self.sentinel):
                #
                # to enforce the schema is correct, we first copy the empty table from the schema template
                # and then append the result to this empty table
                try:
                    assert jobData.handler in self.handlers
                    for key, value in kwargs.items():
                        jobData.instructions[key] = value
                    self.handlers[jobData.handler](**jobData.instructions)
                    self.jobsQueue.task_done()

                except Exception as e:
                    print('Error {} with Jobtype: {}, Instructions: {}'.format(e, jobData.handler, jobData.instructions))
                    raise e

        except Exception as e:
            print("Error {} in self.jobsQueue.get".format(e))
            raise e

    def main_producer_func(self, numExecutors, **kwargs):
        self.producerFunc(numExecutors, self.jobsQueue, **kwargs)
        #
        # Set the sentinel for all processes.
        for i in range(numExecutors):
            self.jobsQueue.put(self.sentinel)  # indicate sentinel

    def run(self, numExecutors=0, **kwargs):
        #
        # main method
        startTime = dt.now()

        if numExecutors==0:
            numExecutors = multiprocessing.cpu_count() * 8

        producer = multiprocessing.Process(name='main_producer_func',
                                           target=self.main_producer_func,
                                           args=(numExecutors,),
                                           kwargs=kwargs)
        producer.start()
        self.jobsQueue.join()
        #
        # initate consumers
        # consumer will execute the job
        consumers = [multiprocessing.Process(name='main_consumer_func',
                                             target=self.main_consumer_func,
                                             args=(i, ),
                                             kwargs=kwargs) for i in range(numExecutors)]
        for c in consumers:
            c.start()

        while True:
            if any(c.is_alive() for c in consumers):
                time.sleep(1)
            else:
                #print('Done')
                break
    #
    # define the job class
    class PCEngineJobData():
        def __init__(self, handler, inst={}):
            self.handler = handler
            self.instructions = inst


def test():
    generator.run(configurations=['Baseball.GameStats.Last7Days'])

#test()
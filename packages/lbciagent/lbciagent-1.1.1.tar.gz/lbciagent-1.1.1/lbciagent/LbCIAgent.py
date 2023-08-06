###############################################################################
# (c) Copyright 2017 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
'''
Command line client that interfaces to the Installer class

:author: Stefan-Gabriel CHITIC
'''
import os
import re
import sys
import logging
import time
from lbciagent import DeploymentPolicy
import lbmessaging
from lbmessaging.exchanges.Common import get_connection, \
    InterruptedProcessing, check_channel
from lbmessaging.exchanges.ContinuousIntegrationExchange import \
    ContinuousIntegrationExchange, PhysBuildReadyMessage, EnvkitReadyMessage
from lbmessaging.exchanges.CvmfsDevExchange import CvmfsDevExchange
from datetime import datetime
import threading
import signal
import traceback


class LbCIAgent(object):
    """
    Global manager for cron like jobs on CVMFS
    """

    def __init__(self, vhost='/lhcb'):
        """
        Before starting any job, verify if this is the only instance
        running
        """

        self.pid = os.getpid()
        self.processors = [{
            'name': 'consume_envkit_ready',
            'converter': self.convertEnvKitMessages,
            'queue': 'EnvKitReadyCIAgent'
        },{
            'name': 'consume_build_ready',
            'converter': self.convertBuildReadyMessages,
            'queue': 'BuildReadyCIAgent'
        },
        ]
        logging.basicConfig(stream=sys.stderr)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.WARNING)

        # Create log first to log starting attempts
        # Setup environment
        self.vhost = vhost
        self.channel = None
        signal.signal(signal.SIGINT, self.signalHandler)
        signal.signal(signal.SIGTERM, self.signalHandler)

    def signalHandler(self, signal=None, stack=None):
        """
        Signals the agent closing
        """
        self.logger.warn("Closing agent")
        if self.channel:
            self.channel.stop_consuming()

    def start(self):
        """
        Starts consuming messages for both build ready and envkit ready
        """
        try:
            self.logger.warn("Start listening...")
            self.channel = check_channel(get_connection(vhost=self.vhost))
            self.command_broker = CvmfsDevExchange(self.channel)
            with self.channel:
                broker = ContinuousIntegrationExchange(self.channel)
                for processor in self.processors:
                    method = getattr(broker, processor['name'])
                    method(processor['converter'], processor['queue'])
                broker.start_consuming()
        except Exception as e:
            # If an error happens during listening(i.e channel connection lost),
            # wait 30=avg nb of seconds until rabbitmq-server damon restarts
            self.logger.error(e)
            self.logger.warn("Restarting agent")
            time.sleep(30)
            self.start()

    def convertEnvKitMessages(self, full_message):
        """
        Function that converts a env kit ready message to CVMFS command message
        :param full_message: the original EnvkitReadyMessage message
        :return: the converted message
        """
        message = full_message.body
        command = 'env_kit_installer'

        args = [message.flavour, message.platform,
                message.version, message.url]
        priority = lbmessaging.priority(lbmessaging.NORMAL, 1.0)
        self.command_broker.send_command(command, args,
                                         priority=priority)
        self.logger.warn('%s-%s-%s CONVERTED' % (
            message.flavour,
            message.platform,
            message.version))
        return True

    def convertBuildReadyMessages(self, full_message):
        """
        Function that converts a build ready message to CVMFS command message
        :param full_message: the original PhysBuildReadyMessage message
        :return: the converted message
        """
        message = full_message.body
        message_with_priority = self.filterAndSetPriority(message)
        if not message_with_priority:
            self.logger.warn('%s-%s-%s-%s-P:%s-D:%s DISCARDED' % (
                message.slot, message.build_id, message.platform,
                message.project, message.priority, message.deployment))
            return True

        command = 'installNightlies'
        args = [message_with_priority.slot, message_with_priority.build_id,
                message_with_priority.platform, message_with_priority.project]
        now = datetime.now()
        expiration = (now.replace(hour=23, minute=59,
                                  second=59) - now).total_seconds()
        expiration = int(expiration * 1000)
        self.command_broker.send_command(
            command, args, expiration=expiration,
            priority=int(message_with_priority.priority))
        self.logger.warn('%s-%s-%s-%s-P:%s-D:%s CONVERTED' % (
            message_with_priority.slot,
            message_with_priority.build_id,
            message_with_priority.platform,
            message_with_priority.project,
            message_with_priority.priority,
            message_with_priority.deployment))
        return True

    def filterAndSetPriority(self, message):
        """
        Computes the priority of the message based on slotsOnCVMFS.txt (from
        home dir)
        :param message: the message without priority
        :return: the message with the priority if the message is for CVMFS
                installation or None otherwise.
        """
        if message.deployment is None:
            return None
        if message and 'cvmfs' not in [x.lower() for x in message.deployment]:
            return None

        message_tmp = message._asdict()
        message_tmp['priority'] = DeploymentPolicy.computePriority(
            message.slot, message.platform)
        return PhysBuildReadyMessage(**message_tmp)



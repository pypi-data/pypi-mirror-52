import os
import ast
from math import sin, cos, sqrt, atan2, radians
import sys
from argparse import ArgumentParser
import logging

#i have not covered any exception handling, we can include that for more robust code.

#set logging handlers, logger file, also we can provide file as a cli argument

logger = logging.getLogger("Invite")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('Invitation.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

class Search:

    def read_file(self,filepath):
        # we can use linux command as well to empty the file
        with open('Invitation.log', 'w'):
            pass
        # read the file
        if os.path.isfile(filepath):
            with open(filepath,'r+') as fd:
                listOfCustomer = fd.readlines()
                self._calculate_radian(listOfCustomer)

    def _calculate_radian(self,listOfCustomer):
        """
        Description: calculates the distance from dublin to guest places and returns the
        Id and name of those guest those are under 100 km range.

        :return:
        """
        # convert dublin lat and long to radians
        lat_dub = radians(53.339428)
        lon_dub = radians(-6.257664)
        # approximate radius of earth in km
        R = 6373.0
        invitation_dict = {}
        for var1 in listOfCustomer:
            #convert input to dictionary
            cust_dict = ast.literal_eval(var1)
            lat2 = radians(float(cust_dict['latitude']))
            lon2 = radians(float(cust_dict['longitude']))
            dlon = lon2 - lon_dub
            dlat = lat2 - lat_dub
            var2 = sin(dlat / 2) ** 2 + cos(lat_dub) * cos(lat2) * sin(dlon / 2) ** 2
            cal_distance = 2 * atan2(sqrt(var2), sqrt(1 - var2))
            distance = R * cal_distance
            if distance <100:
                invitation_dict[cust_dict['user_id']] = cust_dict['name']
        logger.info(sorted(invitation_dict.items()))
        return(invitation_dict)


if __name__ == '__main__':
    parser = ArgumentParser(description='Search Customer to invite')
    parser.add_argument('-f','-filepath',type = str,\
                        default="/home/priyanka/PycharmProjects/untitled/invitation/customer.txt",\
                                   help='Customer list file path')

    arguments = parser.parse_args(sys.argv[1:])
    ob1 = Search()
    ob1.read_file(filepath=arguments.f)


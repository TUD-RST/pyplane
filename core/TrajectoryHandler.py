# -*- coding: utf-8 -*-

#    Copyright (C) 2013
#    by Klemens Fritzsche, pyplane@leckstrom.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Klemens Fritzsche'

import numpy as np
import pylab as pl
from scipy import integrate

from core.Logging import myLogger
from core.ConfigHandler import myConfig


class TrajectoryHandler(object):
    def __init__(self, parent):
        self.mySystem = parent
        self.trajectories = []

    #~ def clear_stack(self):
        #~ self.traj_dict = {}

    def plot_trajectory(self, initial_condition, forward=None, backward=None):
        """
            This function plots the solution of the differential equation
            depending on the initial condition.
        """
        if not forward and not backward:
            myLogger.warn_message("Please select forward and/or backward integration!")
            return False

        else:
            tzero = self.mySystem.myPyplane.slider_value()
            traj_integrationtime = float(myConfig.read("Trajectories", "traj_integrationtime"))
            traj_integrationstep = float(myConfig.read("Trajectories", "traj_integrationstep"))
            num = int(traj_integrationtime/traj_integrationstep)
            time = pl.linspace(tzero, traj_integrationtime, num)
            negtime = pl.linspace(tzero, -traj_integrationtime, num)

            trajectory = Trajectory(self.mySystem, initial_condition, tzero)

            if forward:
                # while integrate.ode.successful():
                # self.mySystem.jacobian(initialCondition)

                assert isinstance(initial_condition, list)
                trajectory.x_forward = integrate.odeint(self.mySystem.equation.rhs, initial_condition, time)
                                          #, full_output=1, printmessg=1,       mxstep=20000)

                xvalue = trajectory.x_forward[:, 0]  # extract the x vector
                yvalue = trajectory.x_forward[:, 1]  # extract the dx/dt vector
                # restrict to visible area
                # TODO: read from lineedits / config
                xvalue[xvalue>10]=np.nan
                xvalue[xvalue<-10]=np.nan
                yvalue[yvalue>10]=np.nan
                yvalue[yvalue<-10]=np.nan

                # plot solution in phase plane:
                traj_ppForwardColor = myConfig.read("Trajectories", "traj_ppForwardColor")
                trajectory.forward_yofx = self.mySystem.Phaseplane.Plot.canvas.axes.plot(xvalue, yvalue, traj_ppForwardColor)
                trajectory.forward_tofxy= self.mySystem.Txy.Plot.canvas.axes.plot(xvalue, yvalue,  time, traj_ppForwardColor)

                zero_arrayx = np.array([10]*len(time))
                zero_arrayy = np.array([-10]*len(time))
                if myConfig.get_boolean("3d-plot", "3d_showXProjection"):
                    plot3d_forward_projx = self.mySystem.Txy.Plot.canvas.axes.plot(xvalue, zero_arrayx, time, "0.75")
                    trajectory.forward_projx = plot3d_forward_projx #
                if myConfig.get_boolean("3d-plot", "3d_showYProjection"):
                    plot3d_forward_projy = self.mySystem.Txy.Plot.canvas.axes.plot(zero_arrayy, yvalue, time, "0.75")
                    trajectory.forward_projy = plot3d_forward_projy #
                if myConfig.get_boolean("3d-plot", "3d_showYXProjection"):
                    plot3d_forward_projxy = self.mySystem.Txy.Plot.canvas.axes.plot(xvalue, yvalue, tzero, "0.75")
                    trajectory.forward_projxy = plot3d_forward_projxy #

                # numpy array with both x and y values in pairs
                # TODO: might be faster if xvalues or yvalues greater than self.mySystem.max_norm
                # are masked before calculating the norm

                #~ xvalue, yvalue = self.filter_values(xvalue, yvalue)

                # plot solution in x(t) and y(t):
                trajectory.forward_xoft = self.mySystem.Xt.Plot.canvas.axes.plot(time, xvalue, color=traj_ppForwardColor)
                trajectory.forward_yoft = self.mySystem.Yt.Plot.canvas.axes.plot(time, yvalue, color=traj_ppForwardColor)

            if backward:
                trajectory.x_backward = integrate.odeint(self.mySystem.equation.rhs, initial_condition, negtime)
                #, full_output=1, printmessg=1)#, mxstep=5000)
                # self.x_bw, infodict2 = integrate.odeint(self.mySystem.n_rhs,
                # initialCondition, self.t)#, full_output=1, printmessg=1)#, mxstep=5000)
                #~ trajectory.x_backward = self.x_bw

                xvalue_bw = trajectory.x_backward[:, 0]
                yvalue_bw = trajectory.x_backward[:, 1]

                # restrict to visible area
                # TODO: read from lineedits / config
                xvalue_bw[xvalue_bw>10]=np.nan
                xvalue_bw[xvalue_bw<-10]=np.nan
                yvalue_bw[yvalue_bw>10]=np.nan
                yvalue_bw[yvalue_bw<-10]=np.nan

                # plot in phase plane:
                traj_ppBackwardColor = myConfig.read("Trajectories", "traj_ppBackwardColor")
                trajectory.backward_yofx = self.mySystem.Phaseplane.Plot.canvas.axes.plot(xvalue_bw, yvalue_bw, color=traj_ppBackwardColor)
                trajectory.backward_tofxy = self.mySystem.Txy.Plot.canvas.axes.plot(xvalue_bw, yvalue_bw,  negtime, traj_ppBackwardColor)

                zero_arrayx = np.array([10]*len(time))
                zero_arrayy = np.array([-10]*len(time))
                if myConfig.get_boolean("3d-plot", "3d_showXProjection"):
                    plot3d_backward_projx = self.mySystem.Txy.Plot.canvas.axes.plot(xvalue_bw, zero_arrayx, negtime, "0.75")
                    trajectory.backward_projx = plot3d_backward_projx
                if myConfig.get_boolean("3d-plot", "3d_showYProjection"):
                    plot3d_backwardprojy = self.mySystem.Txy.Plot.canvas.axes.plot(zero_arrayy, yvalue_bw, negtime, "0.75")
                    trajectory.backward_projy = plot3d_backwardprojy
                if myConfig.get_boolean("3d-plot", "3d_showYXProjection"):
                    plot3d_backward_projxy = self.mySystem.Txy.Plot.canvas.axes.plot(xvalue_bw, yvalue_bw, 0, "0.75")
                    trajectory.backward_projxy = plot3d_backward_projxy

                # plot solution in x(t) and y(t):
                trajectory.backward_xoft = self.mySystem.Xt.Plot.canvas.axes.plot(negtime, xvalue_bw, color=traj_ppBackwardColor)
                trajectory.backward_yoft = self.mySystem.Yt.Plot.canvas.axes.plot(negtime, yvalue_bw, color=traj_ppBackwardColor)

            # mark init:
            if myConfig.get_boolean("Trajectories", "traj_plotInitPoint"):
                traj_initPointColor = myConfig.read("Trajectories", "traj_initPointColor")
                trajectory.init_2d = self.mySystem.Phaseplane.Plot.canvas.axes.plot(initial_condition[0],
                                               initial_condition[1],
                                               '.',
                                               color=traj_initPointColor)
                                    
                trajectory.init_3d = self.mySystem.Txy.Plot.canvas.axes.plot([initial_condition[0]],
                                                                           [initial_condition[1]],
                                                                           [tzero],
                                                                           '.',
                                                                           color=traj_initPointColor)

            self.trajectories.append(trajectory)

            self.mySystem.update()

    def filter_values(self, xvalue, yvalue):
        z = np.column_stack((xvalue, yvalue))

        # put norm of each pair in numpy array
        normed_z = np.array([np.linalg.norm(v) for v in z])

        # masking
        max_norm = self.mySystem.equation.max_norm
        masked_normed_z = np.ma.masked_greater(normed_z, max_norm)
        myMask = masked_normed_z.mask

        # new xvalue and yvalue
        xvalue = np.ma.array(xvalue, mask=myMask)
        yvalue = np.ma.array(yvalue, mask=myMask)

        return xvalue, yvalue

    def create_trajectory(self):
        try:
            initial_condition = self.mySystem.Phaseplane.read_init()
            forward, backward = self.mySystem.Phaseplane.trajectory_direction()

            cond1 = initial_condition[0] is not None
            cond2 = initial_condition[1] is not None
            # check if trajectory with initial_condition exists already
            cond3 = not str(initial_condition) in self.traj_dict

            if cond1 and cond2 and cond3:
                self.plot_trajectory(initial_condition, forward, backward)
                myLogger.message("New initial condition: " + str(initial_condition[0]) + ", " + str(initial_condition[1]))

        except Exception as error:
            myLogger.error_message("Could not create trajectory")
            myLogger.debug_message(str(type(error)))
            myLogger.debug_message(str(error))

    def get_trajectory(self, init, tzero):
        for i in self.trajectories:
            if i.initpos == init and i.t0 == tzero:
                return i
        return None

    def remove_trajectory(self, init, tzero):
        trajectory = self.get_trajectory(init, tzero)
        if trajectory != None:
            trajectory.remove()

    def remove_all(self):
        for i in self.trajectories:
            i.remove()
        self.trajectories = []
        self.mySystem.update()

    def mark_points_in_time(self, time):
        for i in self.trajectories:
            i.mark_point(time)
        self.mySystem.update()

    def remove_marked_points(self):
        for i in self.trajectories:
            i.remove_marked_point()
        self.mySystem.update()
            
class Trajectory(object):
    def __init__(self, mySystem, initpos, t0):
        self.mySystem = mySystem
        self.initpos = initpos
        self.t0 = t0
        self.x_forward = None # raw data
        self.x_backward = None # raw data

        # 2d
        self.init_2d = None

        self.forward_yofx = None
        self.forward_yoft = None
        self.forward_xoft = None

        self.backward_yofx = None
        self.backward_yoft = None
        self.backward_xoft = None        

        # 3d
        self.init_3d = None

        self.forward_tofxy = None
        self.forward_projx = None
        self.forward_projy = None
        self.forward_projxy = None

        self.backward_tofxy = None
        self.backward_projx = None
        self.backward_projy = None
        self.backward_projxy = None

        self.marked_point2d = None
        self.vertical_marker_xt = None
        self.vertical_marker_yt = None
        self.marked_point3d = None
        
    def remove(self):
        self.trajlist = [   self.init_2d,
                            self.forward_yofx,
                            self.forward_yoft,
                            self.forward_xoft,
                            self.backward_yofx,
                            self.backward_yoft,
                            self.backward_xoft,
                            self.init_3d,
                            self.forward_tofxy,
                            self.forward_projx,
                            self.forward_projy,
                            self.forward_projxy,
                            self.backward_tofxy,
                            self.backward_projx,
                            self.backward_projy,
                            self.backward_projxy ]

        for i in self.trajlist:
            if i!=None:
                try:
                    i.pop().remove()
                except Exception as error:
                    myLogger.error_message("An " + str(type(error)) + " error occured while removing a trajectory: " + str(error))

        self.remove_marked_point()

    def remove_marked_point(self):
        if self.marked_point2d != None:
            #~ try:
            self.marked_point2d.pop().remove()
            #~ except:
                #~ pass
        
        if self.vertical_marker_xt != None:
            #~ try:
            self.vertical_marker_xt.remove()
            #~ except:
                #~ pass

        if self.vertical_marker_yt != None:
            #~ try:
                self.vertical_marker_yt.remove()
            #~ except:
                #~ pass
        
        if self.marked_point3d != None:
            #~ try:
            self.marked_point3d.pop().remove()
            #~ except:
                #~ pass

    def mark_point(self, time):
        # this should not be called here:
        # either there are no points yet, or their data should be
        # modified using set_data(..)
        # anyway, the conventions for this method seem to differ
        # (see below)
        self.remove_marked_point()

        # search correct point in numpy array:
        traj_integrationtime = float(myConfig.read("Trajectories", "traj_integrationtime"))
        traj_integrationstep = float(myConfig.read("Trajectories", "traj_integrationstep"))
        num = int(traj_integrationtime/traj_integrationstep)
        if time>self.t0:
            # use self.x_forward
            time_array = pl.linspace(self.t0, traj_integrationtime, num)
            time_ = self.find_nearest_value_in_array(time_array, time)
            index = np.where(time_array==time_)
            xx, yy = self.x_forward[index][0]
        elif time<self.t0:
            # use self.x_backward
            negtime_array = pl.linspace(self.t0, -traj_integrationtime, num)
            time_ = self.find_nearest_value_in_array(negtime_array, time)
            index = np.where(negtime_array==time_)
            xx, yy = self.x_backward[index][0]
        else:
            xx, yy = self.initpos
            time_ = 0

        # 2d plot
        traj_marked_point_color = 'k' # TODO: read from config
        #~ if self.marked_point2d == None:
        self.marked_point2d = self.mySystem.Phaseplane.Plot.canvas.axes.plot(xx, yy, '.',
                                            color=traj_marked_point_color)
        #~ else:
            #~ self.marked_point2d.set_data([xx,yy])
        # vertical marker in x(t) and y(t)
        self.vertical_marker_xt = self.mySystem.Xt.Plot.canvas.axes.axvline(x=time, color='0.75')
        self.vertical_marker_yt = self.mySystem.Yt.Plot.canvas.axes.axvline(x=time, color='0.75')

        # 3d plot
        self.marked_point3d = self.mySystem.Txy.Plot.canvas.axes.plot([xx], [yy], [time_], '.',
                                            color=traj_marked_point_color)
        #~ -> doesn't work for some reason..
        #~ self.vertical_marker_xt.set_data([time,0])
        #~ self.vertical_marker_yt.set_data([time]) -> doesn't work for some reason..
        #~ self.marked_point3d[0].set_data([xx,yy,time_])

    def find_nearest_value_in_array(self, array, value):
        # see http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
        assert isinstance(array, np.ndarray)
        idx = (np.abs(array-value)).argmin()
        return array[idx]
               

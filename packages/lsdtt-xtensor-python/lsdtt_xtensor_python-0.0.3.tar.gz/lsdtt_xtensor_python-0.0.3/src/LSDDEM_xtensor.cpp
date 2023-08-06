//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//
// LSDChiTools
// Land Surface Dynamics ChiTools object
//
// An object within the University
//  of Edinburgh Land Surface Dynamics group topographic toolbox
//  for performing various analyses in chi space
//
//
// Developed by:
//  Simon M. Mudd
//  Martin D. Hurst
//  David T. Milodowski
//  Stuart W.D. Grieve
//  Declan A. Valters
//  Fiona Clubb
//  Boris Gailleton
//
// Copyright (C) 2016 Simon M. Mudd 2016
//
// Developer can be contacted by simon.m.mudd _at_ ed.ac.uk
//
//    Simon Mudd
//    University of Edinburgh
//    School of GeoSciences
//    Drummond Street
//    Edinburgh, EH8 9XP
//    Scotland
//    United Kingdom
//
// This program is free software;
// you can redistribute it and/or modify it under the terms of the
// GNU General Public License as published by the Free Software Foundation;
// either version 2 of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY;
// without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU General Public License for more details.
//
// You should have received a copy of the
// GNU General Public License along with this program;
// if not, write to:
// Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor,
// Boston, MA 02110-1301
// USA
//
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#ifndef LSDDEM_xtensor_CPP
#define LSDDEM_xtensor_CPP
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <ctime>
#include <fstream>
#include <queue>
#include <limits>
#include "LSDStatsTools.hpp"
#include "LSDChiNetwork.hpp"
#include "LSDRaster.hpp"
#include "LSDRasterInfo.hpp"
#include "LSDIndexRaster.hpp"
#include "LSDFlowInfo.hpp"
#include "LSDJunctionNetwork.hpp"
#include "LSDIndexChannelTree.hpp"
#include "LSDBasin.hpp"
#include "LSDChiTools.hpp"
#include "LSDParameterParser.hpp"
#include "LSDSpatialCSVReader.hpp"
#include "LSDShapeTools.hpp"
#include "LSDRasterMaker.hpp"

#include <omp.h>

#include "LSDDEM_xtensor.hpp"

#include "xtensor-python/pyarray.hpp"
#include "xtensor-python/pytensor.hpp"
#include "xtensor-python/pyvectorize.hpp"
#include "xtensor/xadapt.hpp"

#include "LSDStatsTools.hpp"

#include "xtensor/xmath.hpp"
#include "xtensor/xarray.hpp"
#include "xtensor/xtensor.hpp"
#include <iostream>
#include <numeric>
#include <cmath>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <tuple>

// struct link exampl;
// {
//   int source_node;
//   int receiving_node;
//   float zpass;
//   int source_basin;
//   int receiving_basin;
// };
// bool operator>( const link& lhs, const link& rhs )
// {
//   return lhs.zpass > rhs.zpass;
// };
// bool operator<( const link& lhs, const link& rhs )
// {
//   return lhs.zpass < rhs.zpass;
// };
// bool operator>=( const link& lhs, const link& rhs )
// {
//   return lhs.zpass >= rhs.zpass;
// };
// bool operator<=( const link& lhs, const link& rhs )
// {
//   return lhs.zpass <= rhs.zpass;
// };


// This empty constructor is just there to have a default one.
void LSDDEM_xtensor::create()
{
  // Initialising empty objects (throw an error if no default constructors in these classes)
  BaseRaster = return_fake_raster();
  PPRaster = return_fake_raster();
  DrainageArea = return_fake_raster();
  DistanceFromOutlet = return_fake_raster();
  chi_coordinates = return_fake_raster();
  FlowAcc = return_fake_indexraster();
  BasinArrays = return_fake_indexraster();
  FlowInfo = return_fake_flowinfo();
  JunctionNetwork = return_fake_junctionnetwork();
  ChiTool = return_fake_chitool();
  std::cout << "I need information to be created!" << std::endl;
  // std::exit(EXIT_FAILURE);
}

// Real constructor for LSDDEM_xtensor object.
// It takes te following arguments, easily accessible when loading a raster with GDAL-like programs
//  tnrows(int): number of row in the raster array
//  tncols(int): number of columns in the raster array
//  txmin(float): minimum X coordinate
//  tymin(float): minimum Y coordinate
//  tcellsize (float): resolution (presumably in metres)
//  tndv(float): No data value
//  data(pytensor, 2D array): the raster array
// Returns: a LSDDEM object (Does not return it but build it)
void LSDDEM_xtensor::create(int tnrows, int tncols, float txmin, float tymin, float tcellsize, float tndv, xt::pytensor<float,2>& data)
{
  // Loading the attributes of the main raster
  nrows = tnrows;
  ncols = tncols;
  xmin = txmin;
  ymin = tymin;
  cellsize = tcellsize;
  NoDataValue = tndv;
  is_preprocessed = false;
  verbose = true; // I'll add it later, I want it to remain True at the moment as there are crucial debugging and warning messages

  // Generating the LSDraster object of the base raster.
  BaseRaster = LSDRaster(nrows, ncols, xmin, ymin, cellsize, NoDataValue, xt_to_TNT(data,nrows,ncols));

  // Initialising empty objects (throw an error if no default constructors in these classes)
  // I think these are not required anymore but I am keeping it at the moment
  PPRaster = return_fake_raster();
  DrainageArea = return_fake_raster();
  DistanceFromOutlet = return_fake_raster();
  chi_coordinates = return_fake_raster();
  FlowAcc = return_fake_indexraster();
  BasinArrays = return_fake_indexraster();
  FlowInfo = return_fake_flowinfo();
  JunctionNetwork = return_fake_junctionnetwork();
  ChiTool = return_fake_chitool();

    // I just need that before
  boundary_conditions = {"n","n","n","n"};
  default_boundary_condition = true; // This is the default and recommended boundary conditions.
  // Can be later explicitely modify

  // Object constructed
}

// The PreProcessing routines wrap raster filling, depression breaching and (TODO) eventual filtering essential to most of the routines
// Parameters:
//    carve(bool): Wanna carve?
//    fill(cool): Wanna fill?
//    min_slope_for_fill(float): If you are filling, it requires a minimum slope to induce to the raster.
// Returns: Nothing, but implement the preprocessed raster in the object
// Authors: B.G.
void LSDDEM_xtensor::PreProcessing(bool carve, bool fill, float min_slope_for_fill)
{
  // Carve the dem first
  if(carve)
  {
    PPRaster = BaseRaster.Breaching_Lindsay2016();
  }
  // If you want to fill on the top of carving (recommended, the carving does not impose a slope on flat surface)
  if(carve && fill)
  {
    PPRaster = PPRaster.fill(min_slope_for_fill);
  }
  // If only filling is required case
  else if (fill){PPRaster = BaseRaster.fill(min_slope_for_fill);}
  // Nothing, then PPRaster is base raster
  else if(carve == false && fill == false){PPRaster = BaseRaster;}
}

// Calculates the FlowInfo object with D8 method
void LSDDEM_xtensor::calculate_FlowInfo()
{
  // Alright that's all I need, let's get the attributes now
  //# FlowInfo contains node ordering and all you need about navigatinfg through donor/receiver through your raster
  FlowInfo = LSDFlowInfo(boundary_conditions, PPRaster);
  //# Flow accumulation represent the number of pixels draining in each pixels
  FlowAcc = FlowInfo.write_NContributingNodes_to_LSDIndexRaster();
  //# FlowAcc can be converted to drainage area if we know the res. Which we do ofc
  DrainageArea = FlowInfo.write_DrainageArea_to_LSDRaster();
  //# I'll need the distance from outet for a lot of application
  DistanceFromOutlet = FlowInfo.distance_from_outlet();
}

// Calculates the FlowInfo object with D-infinity Dinf method
void LSDDEM_xtensor::calculate_FlowInfo_Dinf()
{
  std::cout << "IMPORTANT-WARNING: I havent tested the Dinf approach yet, carful with that." << std::endl;
  // I just need that before
  vector<string> temp_bc(4);
  boundary_conditions = {"n","n","n","n"};
  // Alright that's all I need, let's get the attributes now
  std::vector<LSDRaster> DINFRAST = PPRaster.D_inf_flowacc_DA();
  //# FlowInfo contains node ordering and all you need about navigatinfg through donor/receiver through your raster
  FlowInfo = LSDFlowInfo(boundary_conditions, PPRaster);
  //# Flow accumulation represent the number of pixels draining in each pixels
  FlowAcc = DINFRAST[0];
  //# FlowAcc can be converted to drainage area if we know the res. Which we do ofc
  DrainageArea = DINFRAST[1];
  //# I'll need the distance from outet for a lot of application
  DistanceFromOutlet = FlowInfo.distance_from_outlet();
}

// Calculates the sources node index once for all
// Different wil be available when I'll get the SpectralRaster to work with python
void LSDDEM_xtensor::calculate_channel_heads(std::string method, float min_contributing_pixels)
{
  // Extraction of river heads and subsequent channel network

  //# Simplest method: area threshold: how many accumulated pixels do you want to initiate a channel.
  //# Easily constraniable and suitable for cases where the exact location of channel heads  does not matter (+/-500 m for example)
  if(method == "min_contributing_pixels")
  {
    // Sources contains the node index of each channel heads
    sources = FlowInfo.get_sources_index_threshold(FlowAcc, min_contributing_pixels);
    // I am saving the min_contributing pixel in a global way: I need it for some reasons
    min_cont = min_contributing_pixels;
    if(sources.size()==0){std::cout << "I did not find any sources" << std::endl; exit(EXIT_FAILURE);}
  }
  else
  {
    // Here later will lie the other methods
    std::cout << "FATAL ERROR::Method " << method << " not implemented!" << std::endl;
    std::exit(EXIT_FAILURE);
  }
}

void LSDDEM_xtensor::ingest_channel_head(xt::pytensor<int,1>& these_sources)
{
  std::vector<int> tempsources(these_sources.size());
  sources = tempsources;
  int minimum_there = 9999999999999999; // I need to constrain the number of sources
  for(size_t i=0; i< these_sources.size(); i++)
  {
    int this_node = these_sources[i];
    sources[i]= this_node;
    int row,col;
    FlowInfo.retrieve_current_row_and_col(this_node,row,col);
    if(DrainageArea.get_data_element(row,col)<minimum_there)
      min_cont = DrainageArea.get_data_element(row,col);
  }// done
}


// Junction Network is an object that helps navigating through the river network junction by junction
void LSDDEM_xtensor::calculate_juctionnetwork(){JunctionNetwork = LSDJunctionNetwork(sources, FlowInfo);}

// A method to get outlet of basins (and subsequent drainage network informations) from a list of xy outlets.
void LSDDEM_xtensor::calculate_outlets_locations_from_xy(xt::pytensor<float,1>& tx_coord_BL, xt::pytensor<float,1>& ty_coord_BL, int search_radius_nodes,int threshold_stream_order, bool test_drainage_boundary, bool only_take_largest_basin)
{
  // Internal calculations needd a bunch of temp raster
  std::vector<float> x_coord_BL, y_coord_BL;
  for(size_t i=0; i<tx_coord_BL.size(); i++)
  {
    x_coord_BL.push_back(tx_coord_BL(i));
    y_coord_BL.push_back(ty_coord_BL(i));
  }
  std::vector<int> valid_cosmo_points;         // a vector to hold the valid nodes
  std::vector<int> snapped_node_indices;       // a vector to hold the valid node indices
  std::vector<int> snapped_junction_indices;   // a vector to hold the valid junction indices
  // ACtual localisation of required outlets
  JunctionNetwork.snap_point_locations_to_channels(x_coord_BL, y_coord_BL, search_radius_nodes, threshold_stream_order, FlowInfo, valid_cosmo_points, snapped_node_indices, snapped_junction_indices);
  // std::cout << snapped_junction_indices.size() << std::endl;
  baselevel_junctions = snapped_junction_indices;// saving

  if(baselevel_junctions.size() ==0)
  {
    std::cout << "I DID NOT FIND ANY BASINS, ADAPT YO COORDINATES" << std::endl;
    exit(EXIT_FAILURE);
  }
  // if I found several basins, I am checking if they are nested. Unfortunately we don't support nested basins yet
  if(baselevel_junctions.size() >1)
    baselevel_junctions = JunctionNetwork.Prune_Junctions_If_Nested(baselevel_junctions,FlowInfo, FlowAcc);
  // Do you want to chek if drainage boundaries are within the raster (strongly adviced)
  if(test_drainage_boundary){baselevel_junctions = JunctionNetwork.Prune_Junctions_Edge_Ignore_Outlet_Reach(baselevel_junctions, FlowInfo, PPRaster);}
  // Sometimes you jsut want your largest basin
  if(only_take_largest_basin){baselevel_junctions = JunctionNetwork.Prune_Junctions_Largest(baselevel_junctions, FlowInfo, FlowAcc);}
  // clean the river network
  JunctionNetwork.get_overlapping_channels_to_downstream_outlets(FlowInfo, baselevel_junctions, DistanceFromOutlet, sources_clean, outlet_nodes,baselevel_nodes,10);
}

// Extract basin with oulet location
void LSDDEM_xtensor::calculate_outlets_locations_from_minimum_size(int minimum_basin_size_pixels, bool test_drainage_boundary, bool prune_to_largest)
{
  //Get baselevel junction nodes from the whole network
  std::vector<int> BaseLevelJunctions_Initial = JunctionNetwork.get_BaseLevelJunctions();

  // now prune these by drainage area
  baselevel_junctions = JunctionNetwork.Prune_Junctions_Area(BaseLevelJunctions_Initial, FlowInfo, FlowAcc, minimum_basin_size_pixels);
  if(prune_to_largest)
    baselevel_junctions = JunctionNetwork.Prune_To_Largest_Complete_Basins(baselevel_junctions,FlowInfo, PPRaster, FlowAcc);
  if (test_drainage_boundary)     // now check for edge effects
  {
    baselevel_junctions = JunctionNetwork.Prune_Junctions_Edge_Ignore_Outlet_Reach(baselevel_junctions,FlowInfo, PPRaster);
  }
  JunctionNetwork.get_overlapping_channels_to_downstream_outlets(FlowInfo, baselevel_junctions, DistanceFromOutlet, sources_clean, outlet_nodes,baselevel_nodes,10);
}

void LSDDEM_xtensor::calculate_outlet_location_of_main_basin(bool test_drainage_boundary)
{
  //Get baselevel junction nodes from the whole network
  std::vector<int> BaseLevelJunctions_Initial = JunctionNetwork.get_BaseLevelJunctions();

  if(test_drainage_boundary == false){baselevel_junctions = JunctionNetwork.Prune_Junctions_Largest(BaseLevelJunctions_Initial, FlowInfo, FlowAcc);}
  else
  {
      vector<int> these_junctions = JunctionNetwork.Prune_Junctions_Edge_Ignore_Outlet_Reach(BaseLevelJunctions_Initial,FlowInfo, PPRaster);
      baselevel_junctions = JunctionNetwork.Prune_Junctions_Largest(these_junctions, FlowInfo, FlowAcc);
  }
  JunctionNetwork.get_overlapping_channels_to_downstream_outlets(FlowInfo, baselevel_junctions, DistanceFromOutlet, sources_clean, outlet_nodes,baselevel_nodes,10);
}

void LSDDEM_xtensor::force_all_outlets(bool test_drainage_boundary)
{
  baselevel_junctions = JunctionNetwork.get_BaseLevelJunctions();
  if(test_drainage_boundary)
    baselevel_junctions = JunctionNetwork.Prune_Junctions_Largest(baselevel_junctions, FlowInfo, FlowAcc);
}

void LSDDEM_xtensor::generate_chi(float theta, float A_0)
{
  ChiTool = LSDChiTools(FlowInfo);
  chi_coordinates = FlowInfo.get_upslope_chi_from_multiple_starting_nodes(baselevel_nodes, theta,A_0, min_cont);
  ChiTool.chi_map_automator_chi_only(FlowInfo, sources_clean, outlet_nodes, baselevel_nodes, PPRaster, DistanceFromOutlet, DrainageArea, chi_coordinates);
  // giving the basin informations to the object
  std::vector<int> this_ordered_BL = ChiTool.get_ordered_baselevel();
  for(size_t i=0;i<this_ordered_BL.size();i++)
  {  
    baselevel_nodes_to_BK[this_ordered_BL[i]] = int(i);
    BK_to_baselevel_nodes[int(i)] = this_ordered_BL[i];
    // I NEED TO CHECK THAT TOMORROW
    BLjunctions_to_BK[JunctionNetwork.get_Junction_of_Node(this_ordered_BL[i], FlowInfo)] = int(i);
    BK_to_BLjunctions[int(i)] = JunctionNetwork.get_Junction_of_Node(this_ordered_BL[i], FlowInfo);
    std::cout << JunctionNetwork.get_Junction_of_Node(this_ordered_BL[i], FlowInfo) << " -----." << int(i) << std::endl;    
  }
}

void LSDDEM_xtensor::generate_ksn(int target_nodes, int n_iterations, int skip, int minimum_segment_length, int sigma,int nthreads)
{
  // JunctionNetwork.get_overlapping_channels_to_downstream_outlets(FlowInfo, baselevel_junctions, DistanceFromOutlet, sources, outlet_nodes, baselevel_nodes,30);
  if(nthreads == 0) // WARNING:: Switch that ast number back to one after debugging!!!
    ChiTool.chi_map_automator(FlowInfo, sources_clean, outlet_nodes, baselevel_nodes,PPRaster, DistanceFromOutlet, DrainageArea, chi_coordinates, target_nodes, n_iterations, skip, minimum_segment_length, sigma);
  else
    ChiTool.chi_map_automator(FlowInfo, sources_clean, outlet_nodes, baselevel_nodes,PPRaster, DistanceFromOutlet, DrainageArea, chi_coordinates, target_nodes, n_iterations, skip, minimum_segment_length, sigma, nthreads);

  ChiTool.segment_counter(FlowInfo, 10000000000);
}

std::pair<std::map<std::string, xt::pytensor<float,1> > , std::map<std::string, xt::pytensor<int,1> > > LSDDEM_xtensor::get_channel_gradient_muddetal2014(int target_nodes, int n_iterations, int skip, int minimum_segment_length, int sigma,int nthreads)
{
  LSDChiTools this_Chitools(FlowInfo);
  this_Chitools.chi_map_automator_chi_only(FlowInfo, sources_clean, outlet_nodes, baselevel_nodes, PPRaster, DistanceFromOutlet, DrainageArea, DistanceFromOutlet);

  // JunctionNetwork.get_overlapping_channels_to_downstream_outlets(FlowInfo, baselevel_junctions, DistanceFromOutlet, sources, outlet_nodes, baselevel_nodes,30);
  if(nthreads == 0) // WARNING:: Switch that ast number back to one after debugging!!!
    this_Chitools.chi_map_automator(FlowInfo, sources_clean, outlet_nodes, baselevel_nodes,PPRaster, DistanceFromOutlet, DrainageArea, DistanceFromOutlet, target_nodes, n_iterations, skip, minimum_segment_length, sigma);
  else
    this_Chitools.chi_map_automator(FlowInfo, sources_clean, outlet_nodes, baselevel_nodes,PPRaster, DistanceFromOutlet, DrainageArea, DistanceFromOutlet, target_nodes, n_iterations, skip, minimum_segment_length, sigma, nthreads);

  this_Chitools.segment_counter(FlowInfo, 10000000000);
  // Getting the data
  std::map<std::string, xt::pytensor<float,1> > datFromCT_flaot = this->get_float_ksn_data_ext_ChiTools(this_Chitools);
  std::map<std::string, xt::pytensor<int,1> > datFromCT_int = this->get_int_ksn_data_ext_ChiTools(this_Chitools);

  return std::make_pair(datFromCT_flaot,datFromCT_int);

}

// This function calculate ksn by direct regression of chi-z steepness
std::pair<std::map<std::string, xt::pytensor<float,1> > , std::map<std::string, xt::pytensor<int,1> > > LSDDEM_xtensor::get_ksn_first_order_chi()
{
  // This requires Chitools to already be calculated as it generates the node ordering!
  // Here we collect our data maps, mchi and bchi will be 0 of course.
  std::map<std::string,xt::pytensor<int,1> > tint = this->get_int_ksn_data();
  std::map<std::string,xt::pytensor<float,1> > tflo = this->get_float_ksn_data();
  tflo.erase("m_chi");
  size_t sizla = tint["nodeID"].size();
  std::array<size_t,1> shape = {sizla};
  xt::xtensor<float,1> ksn_FO(shape);
  // iterating through my nodes
  for(size_t i=0; i<sizla; i++)
  {
    int this_node = tint["nodeID"][i];
    int row,col;
    FlowInfo.retrieve_current_row_and_col(this_node,row,col);
    int recnode; FlowInfo.retrieve_receiver_information(this_node,recnode);
    int rrow, rcol;
    FlowInfo.retrieve_current_row_and_col(recnode, rrow,rcol);
    // Calculating dz/dchi
    ksn_FO[i] = (PPRaster.get_data_element(row,col) - PPRaster.get_data_element(rrow,rcol)) / (PPRaster.get_data_element(row,col) - PPRaster.get_data_element(rrow,rcol)); 

  }

  tflo["ksn"] = ksn_FO;
  return std::make_pair(tflo,tint);
}

// // This Function calculates ksn from regression of chi-z data
// std::pair<std::map<std::string, xt::pytensor<float,1> > , std::map<std::string, xt::pytensor<int,1> > > LSDDEM_xtensor::get_ksn_regression_chi(int half_n_node_reg)
// {
//   // This requires Chitools to already be calculated as it generates the node ordering!
//   // Here we collect our data maps, mchi and bchi will be 0 of course.
//   std::map<std::string,xt::pytensor<int,1> > tint = this->get_int_ksn_data();
//   std::map<std::string,xt::pytensor<float,1> > tflo = this->get_float_ksn_data();
//   tflo.erase("m_chi");
//   size_t sizla = tint["nodeID"].size();
//   std::array<size_t,1> shape = {sizla};
//   xt::xtensor<float,1> ksn_reg(shape);
//   // iterating through my rivers
//   int this_SK = tint["source_key"][0]; int last_SK = -1;
//   for(size_t i=0; i<sizla; i++)
//   {
//     int this_node = tint["nodeID"][i];
//     int row,col;
//     FlowInfo.retrieve_current_row_and_col(this_node,row,col);
//     this_SK = tint["source_key"][i];
//     // If I changed river
//     if(this_SK != last_SK)
//     {
      

//     }

//     int last_node;
//     int recnode; FlowInfo.retrieve_receiver_information(this_node,recnode);
//     int rrow, rcol;
//     FlowInfo.retrieve_current_row_and_col(recnode, rrow,rcol);
//     // Calculating dz/dchi
//     ksn_reg[i] = (PPRaster.get_data_element(row,col) - PPRaster.get_data_element(rrow,rcol)) / (PPRaster.get_data_element(row,col) - PPRaster.get_data_element(rrow,rcol)); 

//   }

//   tflo["ksn"] = ksn_reg;
//   return std::make_pair(tflo,tint);
// }



void LSDDEM_xtensor::detect_knickpoint_locations( float MZS_th, float lambda_TVD,int stepped_combining_window,int window_stepped, float n_std_dev, int kp_node_search)
{
  ChiTool.ksn_knickpoint_automator_no_file(FlowInfo, MZS_th, lambda_TVD,stepped_combining_window,window_stepped, n_std_dev, kp_node_search);
}

TNT::Array2D<float> LSDDEM_xtensor::xt_to_TNT(xt::pytensor<float,2>& myarray, size_t nrows, size_t ncols)
{
  TNT::Array2D<float> lsdata(nrows, ncols, NoDataValue);
  for(size_t i = 0; i< nrows; i++)
  for(size_t j = 0; j< ncols; j++)
  {
    lsdata[i][j] = myarray(i,j);
  }
  return lsdata;
}


// Get chi raster, testing purposes
xt::pytensor<float,2> LSDDEM_xtensor::get_chi_raster()
{
  std::array<size_t,2> shape = {nrows,ncols};
  xt::xtensor<float,2> output(shape);

  for(size_t i=0;i<nrows;i++)
  for(size_t j=0;j<ncols;j++)
  {output(i,j) = chi_coordinates.get_data_element(i,j);}

  return output;
}

// Get chi raster, testing purposes
xt::pytensor<int,2> LSDDEM_xtensor::get_chi_basin()
{
  std::array<size_t,2> shape = {nrows,ncols};
  xt::xtensor<int,2> output(shape);
  LSDIndexRaster garg = ChiTool.get_basin_raster(FlowInfo, JunctionNetwork, baselevel_junctions);
  for(size_t i=0;i<nrows;i++)
  for(size_t j=0;j<ncols;j++)
  {
    int val = garg.get_data_element(i,j), val2 = -9999;
    if(val != -9999)
      val2 = BLjunctions_to_BK[val];
    output(i,j) = val2;
  }


  return output;
}

void LSDDEM_xtensor::already_preprocessed(){is_preprocessed = true; PPRaster = BaseRaster;}
// void LSDDEM_xtensor::already_preprocessed(){is_preprocessed = true; std::unique_ptr<LSDRaster> PPRaster = std::make_unique<LSDRaster>(BaseRaster);}


std::map<std::string, xt::pytensor<int,1> > LSDDEM_xtensor::get_int_ksn_data()
{
  std::map<std::string, std::vector<int> > datFromCT = ChiTool.get_integer_vecdata_for_m_chi(FlowInfo);
  std::map<std::string, xt::pytensor<int,1> > output;

  for(std::map<std::string, std::vector<int> >::iterator it = datFromCT.begin(); it!= datFromCT.end(); it++)
  {
    std::string denom = it->first;
    std::vector<int> denomnomnom = it->second;

    std::array<size_t,1> siz = {denomnomnom.size()};
    xt::xtensor<int,1> this_denomnomnom(siz);
    this_denomnomnom = xt::adapt(denomnomnom,siz);
    output[denom] = this_denomnomnom;
  }

  return output;
}

std::map<std::string, xt::pytensor<int,1> > LSDDEM_xtensor::get_int_ksn_data_ext_ChiTools(LSDChiTools& this_Chitools)
{
  std::map<std::string, std::vector<int> > datFromCT = this_Chitools.get_integer_vecdata_for_m_chi(FlowInfo);
  std::map<std::string, xt::pytensor<int,1> > output;

  for(std::map<std::string, std::vector<int> >::iterator it = datFromCT.begin(); it!= datFromCT.end(); it++)
  {
    std::string denom = it->first;
    std::vector<int> denomnomnom = it->second;

    std::array<size_t,1> siz = {denomnomnom.size()};
    xt::xtensor<int,1> this_denomnomnom(siz);
    this_denomnomnom = xt::adapt(denomnomnom,siz);
    output[denom] = this_denomnomnom;
  }

  return output;
}

std::map<std::string, xt::pytensor<int,1> > LSDDEM_xtensor::get_int_knickpoint_data()
{
  std::map<std::string, std::vector<int> > datFromCT = ChiTool.get_integer_vecdata_for_knickpoint_analysis(FlowInfo);
  std::map<std::string, xt::pytensor<int,1> > output;

  for(std::map<std::string, std::vector<int> >::iterator it = datFromCT.begin(); it!= datFromCT.end(); it++)
  {
    std::string denom = it->first;
    std::vector<int> denomnomnom = it->second;

    std::array<size_t,1> siz = {denomnomnom.size()};
    xt::xtensor<int,1> this_denomnomnom(siz);
    this_denomnomnom = xt::adapt(denomnomnom,siz);
    output[denom] = this_denomnomnom;
  }

  return output;
}

std::map<std::string, xt::pytensor<float,1> > LSDDEM_xtensor::get_float_ksn_data()
{
  std::map<std::string, std::vector<float> > datFromCT = ChiTool.get_float_vecdata_for_m_chi(FlowInfo);
  std::map<std::string, xt::pytensor<float,1> > output;

  for(std::map<std::string, std::vector<float> >::iterator it = datFromCT.begin(); it!= datFromCT.end(); it++)
  {
    std::string denom = it->first;
    std::vector<float> denomnomnom = it->second;

    std::array<size_t,1> siz = {denomnomnom.size()};
    xt::xtensor<float,1> this_denomnomnom(siz);
    this_denomnomnom = xt::adapt(denomnomnom,siz);
    output[denom] = this_denomnomnom;
  }

  return output;
}

std::map<std::string, xt::pytensor<float,1> > LSDDEM_xtensor::get_float_ksn_data_ext_ChiTools(LSDChiTools& this_Chitools)
{
  std::map<std::string, std::vector<float> > datFromCT = this_Chitools.get_float_vecdata_for_m_chi(FlowInfo);
  std::map<std::string, xt::pytensor<float,1> > output;

  for(std::map<std::string, std::vector<float> >::iterator it = datFromCT.begin(); it!= datFromCT.end(); it++)
  {
    std::string denom = it->first;
    std::vector<float> denomnomnom = it->second;

    std::array<size_t,1> siz = {denomnomnom.size()};
    xt::xtensor<float,1> this_denomnomnom(siz);
    this_denomnomnom = xt::adapt(denomnomnom,siz);
    output[denom] = this_denomnomnom;
  }

  return output;
}

std::map<std::string, xt::pytensor<float,1> > LSDDEM_xtensor::get_float_knickpoint_data()
{
  std::map<std::string, std::vector<float> > datFromCT = ChiTool.get_float_vecdata_for_knickpoint_analysis(FlowInfo);
  std::map<std::string, xt::pytensor<float,1> > output;

  for(std::map<std::string, std::vector<float> >::iterator it = datFromCT.begin(); it!= datFromCT.end(); it++)
  {
    std::string denom = it->first;
    std::vector<float> denomnomnom = it->second;

    std::array<size_t,1> siz = {denomnomnom.size()};
    xt::xtensor<float,1> this_denomnomnom(siz);
    this_denomnomnom = xt::adapt(denomnomnom,siz);
    output[denom] = this_denomnomnom;
  }

  return output;
}

// Empty LSDTT constructors
LSDRaster LSDDEM_xtensor::return_fake_raster()
{
  TNT::Array2D<float> tempTNT(2,2,-9999);
  return LSDRaster(2,2,0,0,1,-9999,tempTNT);
}
LSDIndexRaster LSDDEM_xtensor::return_fake_indexraster()
{
  TNT::Array2D<int> tempTNT(2,2,-9999);
  return LSDIndexRaster(2,2,0,0,1,-9999,tempTNT);
}
LSDFlowInfo LSDDEM_xtensor::return_fake_flowinfo()
{
  return LSDFlowInfo(BaseRaster);
}
  LSDChiTools LSDDEM_xtensor::return_fake_chitool()
{
  return LSDChiTools(FlowInfo);
}
LSDJunctionNetwork LSDDEM_xtensor::return_fake_junctionnetwork()
{
  return LSDJunctionNetwork();
}

xt::pytensor<float,2> LSDDEM_xtensor::get_hillshade(float hs_altitude, float hs_azimuth, float hs_z_factor)
{
  LSDRaster hs_raster;
  if(is_preprocessed)
    hs_raster = PPRaster.hillshade(hs_altitude,hs_azimuth,hs_z_factor);
  else
    hs_raster = BaseRaster.hillshade(hs_altitude,hs_azimuth,hs_z_factor);

  std::array<size_t,2> shape = {nrows,ncols};
  xt::xtensor<int,2> output(shape);
  for(size_t i=0;i<nrows;i++)
  for(size_t j=0;j<ncols;j++)
  {output(i,j) = hs_raster.get_data_element(i,j);}

  return output;
}

// Version of hillshading for custom raster
xt::pytensor<float,2> LSDDEM_xtensor::get_hillshade_custom(xt::pytensor<float,2>& datrast, float hs_altitude, float hs_azimuth, float hs_z_factor)
{

  LSDRaster hs_raster, tohillshade = LSDRaster(nrows, ncols, xmin, ymin, cellsize, NoDataValue, xt_to_TNT(datrast,nrows,ncols));
  hs_raster = tohillshade.hillshade(hs_altitude,hs_azimuth,hs_z_factor);
  std::array<size_t,2> shape = {nrows,ncols};
  xt::xtensor<int,2> output(shape);
  for(size_t i=0;i<nrows;i++)
  for(size_t j=0;j<ncols;j++)
  {output(i,j) = hs_raster.get_data_element(i,j);}

  return output;
}


std::vector<xt::pytensor<float,2> > LSDDEM_xtensor::get_polyfit_on_topo(float window, std::vector<int> selecao)
{
  //        0 -> Elevation (smoothed by surface fitting)
//        1 -> Slope
//        2 -> Aspect
//        3 -> Curvature
//        4 -> Planform Curvature
//        5 -> Profile Curvature
//        6 -> Tangential Curvature
//        7 -> Stationary point classification (1=peak, 2=depression, 3=saddle)
  vector<LSDRaster> preoutput;
  if(is_preprocessed)
  {
    preoutput = PPRaster.calculate_polyfit_surface_metrics(window, selecao);
  }
  else
  {
    preoutput = BaseRaster.calculate_polyfit_surface_metrics(window, selecao);
  }

  std::vector<xt::pytensor<float,2> > output;
  for(size_t t=0; t<preoutput.size();t++)
  {
    if(selecao[t]==1)
    {
      std::array<size_t,2> size = {nrows,ncols};
      xt::xtensor<float,2> temparray(size);
      for(size_t i=0;i<nrows;i++)
      for(size_t j=0;j<ncols;j++)
      {temparray(i,j) = preoutput[t].get_data_element(i,j);}
      output.push_back(temparray);
      preoutput[t] = return_fake_raster();
    }
    else
    {
      std::array<size_t,2> size = {0,0};
      xt::xtensor<float,2> temparray(size);
      output.push_back(temparray);
    }
  }
  return output;
}

// This function extract the perimeter for each basin previously extraced.
// return a map with node-x-y-basin_key
std::map<int, std::map<std::string,xt::pytensor<float, 1> > > LSDDEM_xtensor::get_catchment_perimeter()
{
  // initialising the output
  std::map<int,std::map<std::string,xt::pytensor<float, 1> > > output;
  // now iterating through my basins
  int cpt = 0;
  for(std::vector<int>::iterator it = baselevel_junctions.begin(); it != baselevel_junctions.end(); it++)
  {
    LSDBasin thisBasin(*it,FlowInfo, JunctionNetwork);
    thisBasin.set_Perimeter(FlowInfo);
    std::vector<int> these_node = thisBasin.get_Perimeter_nodes();
    std::array<size_t,1> shape = {these_node.size()};
    xt::xtensor<int,1> perinode(shape), perirow(shape), pericol(shape);
    xt::xtensor<float,1> perix(shape), periy(shape), perielev(shape), perikey(shape);
    int cpt2 = 0;
    for (std::vector<int>::iterator it2 = these_node.begin(); it2 != these_node.end(); it2++)
    {
      int this_node = *it2;
      perinode[cpt2] = this_node;
      int row,col;
      FlowInfo.retrieve_current_row_and_col(this_node,row,col);
      perirow[cpt2] = row;
      pericol[cpt2] = col;
      perikey[cpt2] = float(cpt); // basin_key
      float tx,ty;
      FlowInfo.get_x_and_y_from_current_node(this_node,tx,ty);
      perix[cpt2] = tx;
      periy[cpt2] = ty;
      perielev[cpt2] = PPRaster.get_data_element(row,col);
      cpt2++;
    }

    std::map<std::string,xt::pytensor<float, 1> > temp_ou;
    // temp_ou["node"] = perinode;
    // temp_ou["row"] = perirow;
    // temp_ou["col"] = pericol;
    temp_ou["x"] = perix;
    temp_ou["y"] = periy;
    temp_ou["elevation"] = perielev;
    temp_ou["basin_key"] = perikey;
    output[perikey[0]] = temp_ou;
    std::cout << perikey[0] << std::endl;

    cpt++;
  }
  return output;

}

void LSDDEM_xtensor::calculate_movern_disorder(float start_movern, float delta_movern, float n_movern, float A_0, float area_threshold)
{
  // Creating a temporary chitool 
  LSDChiTools ChiTool_disorder(FlowInfo);
  // Calculating the temporary chitool param
  ChiTool_disorder.chi_map_automator_chi_only(FlowInfo, sources_clean, outlet_nodes, baselevel_nodes,
                        PPRaster, DistanceFromOutlet, DrainageArea, chi_coordinates);

  // this map will store the uncertainties results
  std::map<int, std::vector<float> > best_fit_movern_for_basins;
  std::map<int, std::vector<float> > lowest_disorder_for_basins;

  //Getting the ordered base level
  std::vector<int> this_ordered_BL = ChiTool_disorder.get_ordered_baselevel();


  // creating the chi disorder vector of values
  std::vector<float> movern;
  for(int i=0; i<n_movern; i++)
    movern.push_back(start_movern + float(i)*delta_movern);

  associated_movern_disorder = movern;// saving this information
  // movern list ready to go  
  std::vector<std::vector<float> > movern_per_BK(this_ordered_BL.size());
  for(size_t j=0;j<movern_per_BK.size();j++)
  {
    std::vector<float> temp;
    movern_per_BK[j] = temp;
  }

  for(size_t i=0; i<n_movern; i++)
  {  
    if(verbose==true)
      std::cout << "Disorder movern for theta=" << movern[i] << " ..." << std::endl;
    // recalculating chi for this movern
    LSDRaster this_chi = FlowInfo.get_upslope_chi_from_all_baselevel_nodes(movern[i], A_0, area_threshold);
    ChiTool_disorder.update_chi_data_map(FlowInfo, this_chi); // updating the chitool object

    // Potential multithreading her
    for(size_t BK =0; BK< this_ordered_BL.size(); BK++)
    {
      movern_per_BK[BK].push_back(ChiTool_disorder.test_collinearity_by_basin_disorder(FlowInfo, BK));
      std::vector<float> disorder_stats = ChiTool_disorder.test_collinearity_by_basin_disorder_with_uncert(FlowInfo, BK);
      // if this is the first m over n value, then initiate the vectors for this basin key
      if (i == 0)
      {
        lowest_disorder_for_basins[BK] = disorder_stats;
        
        int n_combos_this_basin = int(disorder_stats.size());
        std::vector<float> best_fit_movern;
        for(int bf = 0; bf < n_combos_this_basin; bf++)
        {
          best_fit_movern.push_back( movern[i] );
        }
        best_fit_movern_for_basins[BK] = best_fit_movern;
      }
      else
      {
        // loop through all the combos and get the best fit movern
        std::vector<float> existing_lowest_disorder = lowest_disorder_for_basins[BK];
        std::vector<float> existing_best_fit_movern = best_fit_movern_for_basins[BK];
        int n_combos_this_basin = int(disorder_stats.size());
        
        for(int bf = 0; bf < n_combos_this_basin; bf++)
        {
          if (existing_lowest_disorder[bf] > disorder_stats[bf] )
          {
            existing_lowest_disorder[bf] = disorder_stats[bf];
            existing_best_fit_movern[bf] = movern[i];
          }
        }
        lowest_disorder_for_basins[BK] = existing_lowest_disorder;
        best_fit_movern_for_basins[BK] = existing_best_fit_movern;
      }

    }

    if(verbose==true)
      std::cout << "OK" << std::endl;
  }

  for(size_t BK =0; BK< this_ordered_BL.size(); BK++)
  {
    disorder_movern_per_BK[BK] = movern_per_BK[BK];
  }
  best_fits_movern_per_BK = best_fit_movern_for_basins;
  
  // done


  // std::string residuals_name = "EXPLICITELY_DO_NOT_SAVE_THE_OUTPUT";
  // ChiTool_disorder.calculate_goodness_of_fit_collinearity_fxn_movern_using_disorder(FlowInfo, JunctionNetwork,
  //                 start_movern, delta_movern, n_movern, residuals_name, false); // the false emans no uncertainty test. I'll add it later 
}

xt::pytensor<float,1> LSDDEM_xtensor::burn_rast_val_to_xy(xt::pytensor<float,1> X_coord,xt::pytensor<float,1> Y_coord)
{

  std::array<size_t,1> shape = {X_coord.size()};
  xt::xtensor<float,1> output(shape);
  int row,col;
  for(size_t i=0; i< X_coord.size(); i++)
  {
    PPRaster.get_row_and_col_of_a_point(X_coord[i], Y_coord[i], row, col);
    float val = 0;
    if(row == NoDataValue || col == NoDataValue)
      val = NoDataValue;
    else
      val = PPRaster.get_data_element(row,col);
    output[i] = val;
  }
  return output;
}

// Test function to return the perimeter of each basin, the "ridgeline"
std::map<int, std::map<std::string, xt::pytensor<float,1> > > LSDDEM_xtensor::extract_perimeter_of_basins()
{
  std::map<int, std::map<std::string, xt::pytensor<float,1> > > output;

  size_t n_bas = baselevel_junctions.size();
  for(size_t samp = 0; samp<n_bas; samp++)
  {
    
    std::cout << "Analysing catchment ..." << std::endl;
    LSDBasin thisBasin(baselevel_junctions[samp],FlowInfo, JunctionNetwork);
    std::cout << "Getting the perimeter ..." << std::endl;
    thisBasin.set_Perimeter(FlowInfo);
    std::vector<int> permineter_nodes = thisBasin.get_Perimeter_nodes();
    std::cout << "Got it, let me format the data" << std::endl;
    size_t n_node_in_this_perimeter = permineter_nodes.size();
    std::array<size_t,1> sadfkhkjogjtaoehgoaisdfgoih = {n_node_in_this_perimeter};
    xt::xtensor<float,1> X(sadfkhkjogjtaoehgoaisdfgoih), Y(sadfkhkjogjtaoehgoaisdfgoih), Z(sadfkhkjogjtaoehgoaisdfgoih);
    int this_row, this_col; float this_X, this_Y, this_elev;
    for(size_t huile_de_coude = 0; huile_de_coude < n_node_in_this_perimeter; huile_de_coude ++)
    {
      int this_node = permineter_nodes[huile_de_coude];
      FlowInfo.retrieve_current_row_and_col(this_node,this_row,this_col);
      FlowInfo.get_x_and_y_from_current_node(this_node,this_X,this_Y);
      X[huile_de_coude] = this_X;Y[huile_de_coude] = this_Y;Z[huile_de_coude]= PPRaster.get_data_element(this_row,this_col); 
    }

    std::map<std::string, xt::pytensor<float,1> > temp_ou;
    temp_ou["X"] = X;
    temp_ou["Y"] = Y;
    temp_ou["Z"] = Z;
    output[BLjunctions_to_BK[baselevel_junctions[samp]]] = temp_ou;
  }

  return output;
}


std::map<std::string, xt::pytensor<float,1> > LSDDEM_xtensor::get_sources_full()
{
  std::array<size_t,1> sizla = { sources.size() };
  xt::xtensor<float,1> outX(sizla), outY(sizla), outNodes(sizla);
  for(size_t i=0;i<sources.size();i++)
  {
    int this_node = sources[i];
    if(this_node <0)
    {  
          outX[i] = -9999;
          outY[i]=- 9999;
          outNodes[i] = -9999 ;
          continue;
    }
    outNodes[i] = float(this_node);
    float this_X,this_Y;
    FlowInfo.get_x_and_y_from_current_node(this_node,this_X,this_Y);
    outX[i] = this_X;
    outY[i]=this_Y;
  }
  std::map<std::string, xt::pytensor<float,1> > output;
  output["X"] = outX;
  output["Y"] = outY;
  output["nodeID"] = outNodes;
  return output;
}


void LSDDEM_xtensor::calculate_discharge_from_precipitation(int tnrows, int tncols, float txmin, float tymin, float tcellsize, float tndv, xt::pytensor<float,2>& precdata, bool accumulate_current_node)
{

  // First step is to convert back the precipitation raster into LSDRaster
  std::cout << "I am ingesting the precipitation raster. I am drinking it I guess? Right? haha " << std::endl;
  LSDRaster precipitation_raster_original = LSDRaster(tnrows, tncols, txmin, tymin, tcellsize, tndv, xt_to_TNT(precdata, tnrows, tncols));
  std::cout << "Got it" << std::endl;

  // Potential recasting if extents are different
  if(precipitation_raster_original.get_NRows()!= nrows || precipitation_raster_original.get_NCols()!= ncols)
  {
    std::cout << "I now need to recast it to the right extent. I am just resampling vertically, if you need a more fancy method just do it yourself and ingest a raster to the right extent yo!" << std::endl;
    float goulg = 0;
    TNT::Array2D<float> GORIS(nrows,ncols,goulg);
    LSDRaster new_precipitation = LSDRaster(nrows, ncols, xmin, ymin, cellsize, NoDataValue, GORIS);; // copying the original raster
    for(size_t i=0; i<new_precipitation.get_NRows(); i++)
    for(size_t j=0; j<new_precipitation.get_NCols(); j++)
    {
      float x,y;
      new_precipitation.get_x_and_y_locations(i,j,x,y);
      float new_val = precipitation_raster_original.get_value_of_point(x,y);
      new_precipitation.set_data_element(i,j,new_val);
    }
    std::cout << "RECASTED!" << std::endl;
    precipitation_raster_original = new_precipitation;
  }

  std::cout << "Alright let's calculate the Discharge, it will take time" << std::endl;
  float dx = precipitation_raster_original.get_DataResolution();

  // volume precipitation per time precipitation times the cell areas
  precipitation_raster_original.raster_multiplier(dx*dx);

  // discharge accumulates this precipitation
  DrainageArea = FlowInfo.upslope_variable_accumulator_v2(precipitation_raster_original, accumulate_current_node);
  std::cout << "Done with that calculation! Note that I replace the drainage area raster!" << std::endl;

}

// Simple wrapper that returns xy coordinates from row and column
std::pair<xt::pytensor<float,1>,xt::pytensor<float,1> >LSDDEM_xtensor::query_xy_from_rowcol(xt::pytensor<int,1>& row, xt::pytensor<int,1>& col)
{
  // first simply initialise the output
  std::array<size_t,1> sizla = {row.size()};
  xt::xtensor<float,1> Xs(sizla), Ys(sizla);

  // then query my friend
  for(size_t i=0; i< row.size(); i++)
  {
    float tx,ty;
    PPRaster.get_x_and_y_locations(row[i],col[i],tx,ty);
    Xs[i] = tx; Ys[i] = ty;
  }

  std::pair<xt::pytensor<float,1>,xt::pytensor<float,1> > output =  std::make_pair(Xs,Ys);  
  return output;
}


std::map<std::string, xt::pytensor<float, 1> > LSDDEM_xtensor::get_FO_Mchi()
{
  std::map<std::string,  std::vector<int>  > out =  ChiTool.get_integer_vecdata_for_m_chi(FlowInfo);
  std::map<std::string,  xt::pytensor<float, 1>  > recasted_output;
  xt::pytensor<float, 1>  temp_vec_X,temp_vec_Y,temp_vec_FOMC;
  // first I am creating the arrays
  std::array<size_t,1> sizla = {out["nodeID"].size()};
  xt::xtensor<float,1> this_X(sizla),this_Y(sizla),this_FOMC(sizla), this_elev(sizla), this_DA(sizla), this_flow(sizla);
  for(size_t j = 0; j< out["nodeID"].size(); j++)
  {
    int this_node = out["nodeID"][j], row,col,recrow,reccol,recnode; FlowInfo.retrieve_current_row_and_col(this_node,row,col); FlowInfo.retrieve_receiver_information(this_node, recnode,recrow,reccol);
    float dz,dchi,tx,ty, TFOCM;
    if(this_node != recnode)
    {
      dchi = chi_coordinates.get_data_element(row,col) - chi_coordinates.get_data_element(recrow,reccol);
      dz = PPRaster.get_data_element(row,col) - PPRaster.get_data_element(recrow,reccol);
      this_FOMC[j] = dz/dchi;
    }
    else
    {
      this_FOMC[j] = 0;
    }        
    FlowInfo.get_x_and_y_locations(row,col,tx,ty);
    this_X[j] = tx;this_Y[j]=ty;
    this_elev[j] = PPRaster.get_data_element(row,col);
    this_DA[j] = DrainageArea.get_data_element(row,col);
    this_flow[j] = DistanceFromOutlet.get_data_element(row,col);
    temp_vec_X = this_X;
    temp_vec_Y = this_Y;
    temp_vec_FOMC = this_FOMC;
  }



  recasted_output["X"] = temp_vec_X;
  recasted_output["Y"] = temp_vec_Y;
  recasted_output["fo_m_chi"] = temp_vec_FOMC;
  recasted_output["DA"] = this_DA;
  recasted_output["elevation"] = this_elev;
  recasted_output["flow_distance"] = this_flow;

  return recasted_output;
}

void LSDDEM_xtensor::mask_topo(float value, xt::pytensor<float,2> masker)
{

  for(size_t i = 0; i<nrows; i++)
  {
    for(size_t j = 0; j<ncols; j++)
    {
      if(masker(i,j) == value)
        PPRaster.set_data_element(i,j,value);
    }
  }

}


std::tuple<std::vector<xt::pytensor<float,2> >, std::vector<std::map<std::string, float> > > LSDDEM_xtensor::get_individual_basin_raster()
{
  // formatting the outputs
  std::vector<xt::pytensor<float,2> > vec_1;
  std::vector<std::map<std::string, float> > vec_2;
  // getting the base levels
  for(size_t BK =0; BK< baselevel_junctions.size(); BK++)
  {
    std::cout << "DEBUG::PROC BAS " << BK << " FOR EXTRACTION" << std::endl; 
    // First getting the basin
    LSDBasin that_basin(baselevel_junctions[BK], FlowInfo,  JunctionNetwork);
    // getting the array of topo values
    LSDRaster trimmed_rast = that_basin.TrimPaddedRasterToBasin(30, FlowInfo,
                                             PPRaster);
    // Trimming the no data values
    // LSDRaster trimmed_rast = this_rast.RasterTrimmerPadded(30);
    // pushing in the output
    vec_1.push_back(this->LSDRaster_to_xt(trimmed_rast));
    // the saving method needs the following attribute: Z,x_min,x_max,y_min,y_max,res
    std::vector<float> datvec =  trimmed_rast.get_XY_MinMax();
    vec_2.push_back({{"x_min", datvec[0]}, {"y_min", datvec[1]}, {"x_max", datvec[2]}, {"y_max", datvec[3]}, {"res", trimmed_rast.get_DataResolution()} });
  }

  return {vec_1,vec_2};
}

xt::pytensor<float,2> LSDDEM_xtensor::LSDRaster_to_xt(LSDRaster& datrast)
{

  xt::pytensor<float,2> output = xt::zeros<float>({datrast.get_NRows(),datrast.get_NCols()});

  for(size_t i=0; i< datrast.get_NRows(); i++)
  {
    for(size_t j=0; j<datrast.get_NCols() ; j++)
    {
      output(i,j) = datrast.get_data_element(i,j);
    }
  }
  return output;
}


#endif

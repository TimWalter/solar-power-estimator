Solar Branch of Course 9 at Ferienakademie
==========================================

Milestones
------------
* Estimate Radiation on panel
* Estimate Power output of panel
* Optimize Tilt of panel (also potentially location)
* Estimate and include shading loss (in various degrees of detail)
* Integration with Heat pump group:
  * Interface:
    * Input: Time, Location, Weather?
    * Output: Power per time step
* Fit panel orientation to energy demand/costs etc. basically cost function.
* 3D rendering visualization of power cycle

Data & Methodology
-----------------
* Radiation estimation: 
  * Weather data
  * Location: 
    * Latitude
    * Longitude
    * Altitude
  * Orientation: 
    * Azimuth
    * Elevation angle
  * Time
  * Date
  * Timezone?
  * Shadow model:
    * Blender/Google maps

* Power estimation:
  * Panel data (Solar equation)

* Optimization:
  * ADAM optimizer

* Shading:
  * Initially stupid coefficient
  * Pathtracing/Projecting shadows
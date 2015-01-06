# Launch simulation
Launch simulation for Falcon 9 and Falcon Heavy. It should be easily extensible for other rockets (BFR...?) and theoretically it should also be easy to implement fuel cross-feed.

##Acknowledgements
https://github.com/murphd37/SpX for their amazing launch simulations and landing burn (which this repo does not simulate).

##Considerations:
* I'm a high school student, beware of bugs (and flawed physics) in the code!
* Right now it doesn't do any kind of course corrections, just a gravity turn. This makes it much harder to simulate, because even a 1-degree difference in the gravity turn can mean that your rocket will point down (and you're not going to go to space). I've been trying to look for launch trajectory optimizations to a 200x200 km orbit but it seems a lot of it is under export control, so I cannot read it. I'll try to find and implement a trajectory, possibly by abusing Monte Carlo.
* Coefficient of drag taken from murphd37's simulation (0.3), could be incorrect.
* Atmospheric model taken from a NASA website.
* It uses RK4 integration.

## Conclusions
* I was able to put a Falcon 9 into a 316x200 orbit with a payload of 13500 kg and some 5325 kg of fuel to spare. That translates to a total "payload" of 19t, which confirms the extra 30% margin for reusability that Falcon 9 has built in [we have to take the fairings' 1.75t weight to make ends meet, and we should also consider that these 5325 kg of fuel can be burned for extra payload and that the orbit isn't circular].
* Falcon Heavy seems to require a steeper gravity turn, right now it kinda works but to make it really work I'd need a correct launch trajectory (without course corrections it's incredibly hard to get a correct orbit!).
* Now that we have some extra info for BFR we should be able to implement it with this code. It's a matter of creating an Engine() for the Raptor engines and creating the proper Stage()s to make the final Rocket() (see example code).

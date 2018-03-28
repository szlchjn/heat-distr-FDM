# heat-distr-FDM
Finite difference algorithm and API for calculating steady state heat distribution in functionally graded materials (FGMs).
![wykresy](https://user-images.githubusercontent.com/30974121/38013213-a16078f0-3264-11e8-9577-81001096d6da.png)
### Equation
Solves differential, steady state heat transfer equation for one-way-nonhomogeneous materials, with no heat source:
```
rC*dT/dt - d/dx(k1(x)*dT/dx) + k2*d^2T/dy^2 = 0
```
```
k2 = const.
dT/dt = 0
```
### Finite difference method
Approximates partial derrivatives using central difference with local truncation error *O(h^2)*,
and applies five point Laplacian operator stencil with coefficients adjusted for variance in material properties
## Dependencies
```
numpy 1.13.3
matplotlib 2.0.2
```
## Assumptions
1. Domain has rectangular shape 
2. Boundary conditions can be set manually anywhere throughout the domain 
   (provided API only allows setting them on edges of the domain)
3. Heat transfer coefficient (HTC) along x-axis can be a function, but y-axis HTC must be constant
   (material is functionally graded in **only direction parallel to x-axis**)
4. Calculations are time invariant and return stabilized temperature across domain (*dT/dt = 0*)
## API
Run **interface.py** and specify:
* domain size (width, height)
* heat transfer coefficients (kx, ky)
* grid size (h)
* Dirichlet boudary conditions as function (bound)
* apply conditions ([x, 0], [width, y], [x, height], [0, y])

Outputs three plots:
* heat map 
* 3D temperature plot
* lenghtwise cross sections of 3D plot

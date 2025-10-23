![CI Tests](https://github.com/lsiver/swa3_project/workflows/CI%20Tests/badge.svg)
# swa3_project# - Binary Distillation Column
## https://swa3-project-1.onrender.com

## Purpose

The purpose of this application is to perform detailed calculations to figure out the number of  
“stages” (or physical trays) in a distillation tower required to separate two chemical components  
into a light-key component (overhead product) and the heavy-key component (bottoms product).  

As well as performing the calculations, this program also displays the **McCabe-Thiele Diagram**  
from which the results were produced. This is a graph that is generally easier to understand than  
the strictly analytical methods for performing distillation calculations.  

- Each “stair-step” represents a physical tray where liquids/vapor are flashed and further separated.  
- This graph also displays the vapor and liquid composition, in terms of the light-key component, at each stage (with the other component’s composition being 1 - the light-key).  
- As you go “up” the tower/stages, the light-key component becomes the more dominant component and is purified.  

---

## Program Features

- The program allows you to select two components: **Light Key (LK)** or **Heavy Key (HK)**.  
- Generally you want to select two components close to each other in the list since this is a more “difficult” separation.  
  - Choosing *ethane/butane* is a trivial separation.  
  - Choosing *ethane/ethylene* is a very difficult separation and would require many stages.  
- Then the user can select:  
  - The assumed feed composition (in terms of light-key %).  
  - The desired overhead product purity.  
  - The bottoms product purity (in terms of light-key, this should be small).  
  - The reflux ratio.  
  - Then the user can select **Run Simulation**.  

**Note:** Temperature / Pressure conditions are ignored for ideal conditions.  

---

## Idealized Conditions

The calculations can be performed assuming idealized conditions where compressibility / nonideal behavior is ignored.  
This is:  

- Much simpler.  
- Faster.  
- Not affected by tower pressure or tower temperature.  

The basis for this calculation is through using **Raoult’s law**:  

xi * Psat = yi * P

Where:  
- `Psat` is calculated from Antoine’s constants.  
- These constants are scraped / pulled from **NIST’s API** and then stored in an **SQLite database**.  

Rearranging Raoult’s law gives:  

yi/xi = Psat/P = alpha_i (volatility)


By convention, you divide the lighter volatility by the heavier volatility to get the **relative volatility**.  

- A relative volatility for a system > 1.0 is possible to separate the components.  
- As this value becomes closer and closer to 1.0, it becomes more difficult, and possibly impossible at 1.0, to separate the components at current conditions.  
- The easier the separation, the fewer stages/trays are required.  

---

## Non-Ideal Conditions

There is also the option to perform these calculations under non-ideal conditions.  

- This is a much more complicated calculation using the **Peng-Robinson equation of state**.  
- This calculation, in addition to the Antoine’s constants from NIST, also requires:  
  - `Pc` (critical pressure),  
  - `Tc` (critical temperature),  
  - `w` (acentric factor).  

These values are also pulled from NIST.  

The details of this calculation will not be discussed but the calculations are in the backend code.  

![Screenshot](MccabeThiele.png)

### 10/23/2025 
Added docker files. Should be able to run this using docker compose up and then navigate to localhost:3000





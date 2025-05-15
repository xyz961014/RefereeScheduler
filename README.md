# RefereeScheduler

**RefereeScheduler** is a project that automatically assigns referees to football matches based on availability, experience, match importance, and fatigue constraints. It implements **two complementary approaches**:

- **MiniZinc** – classical symbolic solver.
- **LLM (OpenAI o3)** – generative model with reasoning.

### Background

In professional and amateur football leagues, organizing weekend matches requires considerate planning—not just for players and venues, but also for referee assignments. Each match must be officiated by:

- 1 **Main Referee**
- 2 **Assistant Referees**
- 1 **Fourth Official**

Referees vary in **experience**, have different **availability slots**, and are subject to **physical fatigue**—especially if scheduled for multiple high-intensity roles in close succession. At the same time, matches vary in **importance and difficulty**, with matches in higher-tier leagues often demand more experienced referees. The assignment process must balance fairness, efficiency, and quality, while adhering to practical constraints.

Traditionally, these assignments are done manually. This project explores how formal constraint modeling and LLM-based reasoning can automate this process.

### Problem Definition

We aim to schedule referees for a **single day of football matches**, ensuring that each match is properly officiated and all assignments respect referee constraints such as availability, fatigue, and experience.

---

#### Entities and Properties

##### **Game**
Each game is defined by:
- `time_begin`, `time_end`: the scheduled start and end times (e.g., `12:00–14:00`)
- `difficulty_factor`: a numerical value representing match difficulty, influenced by factors such as league tier, competing teams, and possibly other attributes
- `field`: the physical location where the match takes place
- each game requires one main referee, two assistant referees and one fourth official 

##### **Referee**
Each referee is characterized by:
- `available_time_slots`: a set of time intervals during which the referee is available
- `main_ref_experience`: the cumulative difficulty factor of all previously officiated matches as **Main Referee**
- `assistant_ref_experience`: the cumulative difficulty factor of all previously officiated matches as **Assistant Referee**

> *Note: The role of **Fourth Official** does not require experience and is not considered for fatigue.*

---

#### Constraints

1. **No Time Conflicts**  
   A referee cannot be assigned to overlapping matches.
2. **Role Fatigue Limit**  
   A referee may be assigned to **at most two matches** in the roles of **Main Referee** or **Assistant Referee**. Additional assignments are not allowed due to fatigue constraints.
3. **Travel Time Between Fields**  
   If a referee is assigned to consecutive matches at different fields, there must be at least **30 minutes** of travel time between the end of the first match and the start of the next.

---

#### Objective

**Maximize** the overall assignment quality by prioritizing experienced referees for difficult games:

This encourages assigning:
- **Experienced Main Referees** to **high-difficulty matches** as Main Referees
- **Experienced Assistant Referees** similarly for Assistant Referee roles

The objective ensures high-quality officiating while maintaining fairness and feasibility across all assignments.

### Data

The dataset consists of anonymous scheduling data provided by the Tsinghua University Student Football Association. It covers 20 days of football matches.

### Results

<table>
  <tr>
    <th>Data</th>
    <th>#Games</th>
    <th>Method</th>
    <th>Model</th>
    <th>Score</th>
    <th>Time</th>
  </tr>
  <tr>
    <td rowspan="5">2024-03-30</td>
    <td rowspan="5">10</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>0</td>
    <td>10.25</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3759</td>
    <td>60.26</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3781</td>
    <td>120.25</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-03-31</td>
    <td rowspan="5">9</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3044</td>
    <td>10.24</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3085</td>
    <td>60.24</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3122</td>
    <td>120.25</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
    <tr>
    <td rowspan="5">2024-04-06</td>
    <td rowspan="5">11</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>0</td>
    <td>10.27</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>2990</td>
    <td>60.26</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>4171</td>
    <td>120.26</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-04-13</td>
    <td rowspan="5">7</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>2592</td>
    <td>10.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>2819</td>
    <td>60.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>2878</td>
    <td>83.99</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-04-14</td>
    <td rowspan="5">8</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>4294</td>
    <td>10.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>4350</td>
    <td>60.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>4369</td>
    <td>120.23</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-10-12</td>
    <td rowspan="5">8</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3608</td>
    <td>10.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3943</td>
    <td>60.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>4022</td>
    <td>120.23</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-10-13</td>
    <td rowspan="5">9</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>1409</td>
    <td>10.26</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>4202</td>
    <td>60.24</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>4202</td>
    <td>120.25</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-10-20</td>
    <td rowspan="5">9</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>4466</td>
    <td>10.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>4665</td>
    <td>60.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>4687</td>
    <td>120.22</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-11-17</td>
    <td rowspan="5">8</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>1862</td>
    <td>10.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>2138</td>
    <td>60.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>2153</td>
    <td>120.23</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-11-23</td>
    <td rowspan="5">7</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3045</td>
    <td>10.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3126</td>
    <td>60.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3163</td>
    <td>120.23</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2024-11-24</td>
    <td rowspan="5">8</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>2027</td>
    <td>10.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>2027</td>
    <td>60.24</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>2027</td>
    <td>120.22</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-08</td>
    <td rowspan="5">7</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>2398</td>
    <td>10.21</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>2442</td>
    <td>60.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>2478</td>
    <td>120.23</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-09</td>
    <td rowspan="5">8</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3037</td>
    <td>10.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3038</td>
    <td>60.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3081</td>
    <td>120.22</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-16</td>
    <td rowspan="5">11</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3885</td>
    <td>10.24</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3903</td>
    <td>60.24</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3909</td>
    <td>120.24</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-15</td>
    <td rowspan="5">10</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3339</td>
    <td>10.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3347</td>
    <td>60.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3364</td>
    <td>120.24</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-22</td>
    <td rowspan="5">9</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>2982</td>
    <td>10.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3048</td>
    <td>60.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3127</td>
    <td>120.23</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-23</td>
    <td rowspan="5">7</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>2783</td>
    <td>10.22</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>2899</td>
    <td>60.21</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>2899</td>
    <td>120.21</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-29</td>
    <td rowspan="5">12</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3981</td>
    <td>10.27</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3981</td>
    <td>60.25</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3981</td>
    <td>120.25</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-03-30</td>
    <td rowspan="5">8</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>3961</td>
    <td>10.21</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>3961</td>
    <td>60.27</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>3961</td>
    <td>120.22</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">2025-04-20</td>
    <td rowspan="5">6</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>2721</td>
    <td>10.19</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>2796</td>
    <td>25.65</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>2796</td>
    <td>26.11</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td rowspan="5">Total (per game)</td>
    <td rowspan="5">172</td>
    <td rowspan="3">MiniZinc</td>
    <td>chuffed timeout 10s</td>
    <td>322.28</td>
    <td>10.23</td>
  </tr>
  <tr>
    <td>chuffed timeout 60s</td>
    <td>386.74</td>
    <td>58.51</td>
  </tr>
  <tr>
    <td>chuffed timeout 120s</td>
    <td>396.34</td>
    <td>113.72</td>
  </tr>
  <tr>
    <td rowspan="2">LLM</td>
    <td>o3-medium</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>o4-mini-high</td>
    <td></td>
    <td></td>
  </tr>
</table>


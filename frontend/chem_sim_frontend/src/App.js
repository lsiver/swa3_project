import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import './App.css';
import distillationImage from './Tray_Distillation_Tower.PNG';

function App() {
const API_BASE_URL = process.env.NODE_ENV === 'production'
? 'https://swa3-project.onrender.com'
: 'http://127.0.0.1:5001';

  const [parameters, setParameters] = useState({
    component_a: 'Toluene',
    component_b: 'Benzene',
    feed_composition: 0.8,
    distillate_purity: 0.95,
    bottoms_purity: 0.05,
    pressure: 1.0,
    reflux_ratio: 4.0,
    use_idealized: false,
    temperature:405
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const Tooltip = ({ text }) => (
    <span className="tooltip-container">
      <span className="tooltip-icon">?</span>
      <span className="tooltip-text">{text}</span>
    </span>
  );

    const runSimulation = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(parameters)
      });

      const data = await response.json();

      if (data.success) {
        setResults(data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Failed to connect to backend');
    }

    setLoading(false);
    };



    const rescrapeAntoine = async () => {
    setLoading(true);
    setError(null);

    try {
    const response = await fetch(`${API_BASE_URL}/api/rescrapeAntoine`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({flag:1})
    });

    if (response.ok) {
    console.log('Antoine data re-scraped from NIST')}
    const data = await response.json();

    } catch (err) {
    setError('Failed to connect to backend');
    }
    setLoading(false)
    }

const createPlotlyTraces = () => {
  if (!results?.results?.plot_data) return [];

  const traces = [];
  const { plot_data } = results.results;

  // VLE data / curve
  traces.push({
    x: plot_data.vle_curve.x,
    y: plot_data.vle_curve.y,
    type: 'scatter',
    mode: 'lines',
    name: 'VLE Curve',
    line: { color: 'red', width: 3 }
  });

  // x = y line (45 deg)
  traces.push({
    x: [0, 1],
    y: [0, 1],
    type: 'scatter',
    mode: 'lines',
    name: 'y = x',
    line: { color: 'black', dash: 'dash', width: 2 }
  });

  // rectification operating line
  traces.push({
    x: plot_data.rectifying_line.x,
    y: plot_data.rectifying_line.y,
    type: 'scatter',
    mode: 'lines',
    name: 'Rectification Line',
    line: { color: 'blue', width: 2 }
  });

  // stripping section operating line
  traces.push({
    x: plot_data.stripping_line.x,
    y: plot_data.stripping_line.y,
    type: 'scatter',
    mode: 'lines',
    name: 'Stripping Line',
    line: { color: 'green', width: 2 }
  });

  // step points
  const x_stages = results.results.stages.map(stage => stage[0]);
  const y_stages = results.results.stages.map(stage => stage[1]);

  traces.push({
    x: x_stages,
    y: y_stages,
    type: 'scatter',
    mode: 'markers',
    name: 'Theoretical Stages',
    marker: { color: 'purple', size: 8 }
  });

  // mccabe thiele steps
  plot_data.steps.forEach((step, index) => {
    traces.push({
      x: step.x,
      y: step.y,
      type: 'scatter',
      mode: 'lines',
      showlegend: false,
      line: { color: 'lightblue', width: 2 },
      hoverinfo: 'skip'
    });
  });

  // feed stage
  traces.push({
    x: [plot_data.feed_point.x],
    y: [plot_data.feed_point.y],
    type: 'scatter',
    mode: 'markers',
    name: 'Feed Stage',
    marker: { color: 'orange', size: 12, symbol: 'diamond' }
  });

  return traces;
};

  return (
    <div className="App">
      <header className="App-header">
        <h1>Binary Distillation Calculator</h1>
        <img src = {distillationImage}
        alt = "Distillation Column"
        className="header-image"
        />
      </header>

      <div className="main-content">
        <div className="controls-panel">
          <h3>Simulation Parameters</h3>

          <div className="parameter">
            <label>
              Component LK:
              <Tooltip text="Light Key component - The more volatile component that separates at the top" />
            </label>
            <select 
              value={parameters.component_a}
              onChange={(e) => setParameters({...parameters, component_a: e.target.value})}
            >
              <option value="Methane">Methane</option>
              <option value ="Ethane">Ethane</option>
              <option value ="Ethylene">Ethylene</option>
              <option value ="Propane">Propane</option>
              <option value ="Butane">Butane</option>
              <option value ="Pentane">Pentane</option>
              <option value ="Hexane">Hexane</option>
              <option value="Toluene">Toluene</option>
              <option value="Benzene">Benzene</option>
            </select>
          </div>

          <div className="parameter">
            <label>
              Component HK:
              <Tooltip text="Heavy Key component - the less volatile component that is concentrated at the bottom"/>
            </label>
            <select 
              value={parameters.component_b}
              onChange={(e) => setParameters({...parameters, component_b: e.target.value})}
            >
              <option value="Methane">Methane</option>
              <option value ="Ethane">Ethane</option>
              <option value ="Ethylene">Ethylene</option>
              <option value ="Propane">Propane</option>
              <option value ="Pentane">Pentane</option>
              <option value ="Hexane">Hexane</option>
              <option value="Toluene">Toluene</option>
              <option value="Benzene">Benzene</option>
            </select>
          </div>

          <div className="parameter">
            <label>
              Feed Composition (LK): {parameters.feed_composition.toFixed(2)}
              <Tooltip text="Mole fraction of the LK component in the feed stream (0-1)" />
            </label>
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.01"
              value={parameters.feed_composition}
              onChange={(e) => setParameters({
                ...parameters,
                feed_composition: parseFloat(e.target.value)
              })}
            />
          </div>

          <div className="parameter">
            <label>
              Distillate Purity (LK): {parameters.distillate_purity.toFixed(2)}
              <Tooltip text="Desired mole fraction of the LK component in the overhead product. Will be equal to this number" />
            </label>
            <input
              type="range"
              min="0.50"
              max="0.99"
              step="0.01"
              value={parameters.distillate_purity}
              onChange={(e) => setParameters({
                ...parameters,
                distillate_purity: parseFloat(e.target.value)
              })}
            />
          </div>

          <div className="parameter">
            <label>
              Bottoms Purity (LK): {parameters.bottoms_purity.toFixed(3)}
              <Tooltip text="Desired mole fraction of the LK component in the bottom product. Will be less than or equal to this number" />
            </label>
            <input
              type="range"
              min="0.01"
              max="0.2"
              step="0.001"
              value={parameters.bottoms_purity}
              onChange={(e) => setParameters({
                ...parameters,
                bottoms_purity: parseFloat(e.target.value)
              })}
            />
          </div>

          <div className="parameter">
            <label>
              Reflux Ratio: {parameters.reflux_ratio.toFixed(1)}
              <Tooltip text="Reflux ratio of the tower. Ratio of liquid returned to the tower over the distillate product" />
            </label>
            <input
              type="range"
              min="1.1"
              max="30.0"
              step="0.1"
              value={parameters.reflux_ratio}
              onChange={(e) => setParameters({
                ...parameters,
                reflux_ratio: parseFloat(e.target.value)
              })}
            />
          </div>

        <div className="parameter">
          <label>
            Pressure: {parameters.pressure.toFixed(1)}
            <Tooltip text="Tower Pressure. Lower pressure is easier separation but higher condensing costs. In bar" />
          </label>
          <input
            type="range"
            min="0.1"
            max="40"
            step="0.1"
            value={parameters.pressure}
            onChange={(e) => setParameters({
              ...parameters,
              pressure: parseFloat(e.target.value)
            })}
          />
        </div>

        <div className="parameter">
          <label>
            Temperature: {parameters.temperature.toFixed(1)}
            <Tooltip text="Degrees Celsius. Average tower temperature. If the relative volatility is too low, lowering this can help" />
          </label>
          <input
            type="range"
            min="-250"
            max="700"
            step="5"
            value={parameters.temperature}
            onChange={(e) => setParameters({
              ...parameters,
              temperature: parseFloat(e.target.value)
            })}
          />
        </div>

          <div className="parameter checkbox-parameter">
            <label className="checkbox-label">
            <input
              type="checkbox"
              checked={parameters.use_idealized}
              onChange={(e) => setParameters({
                ...parameters,
                use_idealized: e.target.checked
              })}
            />
            <span>Use idealized predictions?</span>
            <Tooltip text="Use idealized vapor-liquid equilibrium predictions instead of peng-robinson detailed calculations. When using idealized, tower pressure and temperature do not affect relative volatility" />
            </label>
          </div>

          <button
            onClick={runSimulation}
            disabled={loading}
            className="run-button"
          >
            {loading ? 'Running Simulation...' : 'RUN SIMULATION'}
          </button>

          <button
            onClick={rescrapeAntoine}
            disabled={loading}
            className="run-button"
          >
            {loading ? 'Collecting latest Antoine data...' : 'Rebuild NIST Antoine DB'}
          </button>

          {error && <div className="error">Error: {error}</div>}
        </div>

        <div className="results-panel">
          {results && (
            <div>
              <div className="results-summary">
                <h3>Simulation Results</h3>
                <div className="results-grid">
                  <div className="result-item">
                    <strong>
                    Actual Stages<Tooltip text="Required number of theoretical trays/stages required at current conditions"/>:
                    </strong> {results.results.stage_count}
                  </div>
                  <div className="result-item">
                    <strong>
                    Minimum Stages (Nmin)<Tooltip text="Stages required if you could operate the tower at total reflux. Theoretical minimum stages"/>:
                    </strong> {results.results.Nmin?.toFixed(1)}
                  </div>
                  <div className="result-item">
                    <strong>
                    Minimum Reflux (Rmin)<Tooltip text="Minimum reflux required in order to avoid creating a pinch-point between the stripping and rectification lines. Below this number, separation is not possible"/>:
                    </strong> {results.results.Rmin?.toFixed(3)}
                  </div>
                  <div className="result-item">
                    <strong>Actual Reflux:</strong> {parameters.reflux_ratio}
                  </div>
                  <div className="result-item">
                    <strong>
                    Relative Volatility (α)<Tooltip text="The ratio of volatilities between the light and heavy key components. Higher values mean easier separation"/>:
                    </strong> {results.results.alpha?.toFixed(3) || 'N/A'}
                  </div>
                </div>

                {results.results.alpha && results.results.alpha <= 1.05 && (
                  <div className="volatility-warning">
                    <strong>Warning:</strong>
                    {results.results.alpha === 1 ? (
                      <span> Separation is <strong>IMPOSSIBLE</strong> at current conditions (α = 1).
                      You MUST change operating conditions: try lowering the temperature or reducing the pressure.</span>
                    ) : (
                      <span> Separation is very difficult (α = {results.results.alpha?.toFixed(3)}).
                      Consider changing operating conditions for better separation: lower temperature or pressure.</span>
                    )}
                  </div>
                )}
              </div>

              <div className="plot-container">
                <h3>McCabe-Thiele Diagram</h3>
                <Plot
                  data={createPlotlyTraces()}
                    layout={{
                      title: {
                        text: `McCabe-Thiele Diagram: ${parameters.component_a}-${parameters.component_b}`,
                        font: { size: 20 }
                      },
                      xaxis: {
                        title: {
                          text: `Liquid Composition, LK (x) - ${parameters.component_a}`,
                          font: { size: 14 }
                        },
                        range: [0, 1],
                        gridcolor: '#f0f0f0',
                        zeroline: true,
                        showline: true,
                        linewidth: 1,
                        linecolor: 'black'
                      },
                      yaxis: {
                        title: {
                          text: `Vapor Composition, LK (y) - ${parameters.component_a}`,
                          font: { size: 14 }
                        },
                        range: [0, 1],
                        gridcolor: '#f0f0f0',
                        zeroline: true,
                        showline: true,
                        linewidth: 1,
                        linecolor: 'black'
                      },
                      showlegend: true,
                      legend: {
                        x: 0.02,
                        y: 0.98,
                        bgcolor: 'rgba(255,255,255,0.8)'
                      },
                      plot_bgcolor: 'white',
                      paper_bgcolor: 'white',
                      autosize: true,
                      margin: {
                        l: 80,
                        r: 50,
                        b: 80,
                        t: 100,
                        pad: 4
                      }
                    }}
                  style={{ width: '100%', height: '700px' }}
                  config={{ responsive: true }}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
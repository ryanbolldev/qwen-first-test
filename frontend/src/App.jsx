import { useState } from 'react'

const App = () => {
  const [file, setFile] = useState(null)
  const [formData, setFormData] = useState({
    gaussian_period: 20,
    gaussian_multiplier: 2.0,
    slope_lookback: 4,
    donchian_period: 20,
    position_size_percent: 1.0,
    initial_capital: 10000.0,
    direction: 'both'
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'gaussian_multiplier' || name === 'position_size_percent' || name === 'initial_capital'
        ? parseFloat(value)
        : name === 'gaussian_period' || name === 'slope_lookback' || name === 'donchian_period'
          ? parseInt(value)
          : value
    }))
  }

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    const formDataObj = new FormData()
    formDataObj.append('file', file)
    formDataObj.append('gaussian_period', formData.gaussian_period)
    formDataObj.append('gaussian_multiplier', formData.gaussian_multiplier)
    formDataObj.append('slope_lookback', formData.slope_lookback)
    formDataObj.append('donchian_period', formData.donchian_period)
    formDataObj.append('position_size_percent', formData.position_size_percent)
    formDataObj.append('initial_capital', formData.initial_capital)
    formDataObj.append('direction', formData.direction)

    try {
      const response = await fetch('http://localhost:8000/backtest/upload', {
        method: 'POST',
        body: formDataObj
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const renderEquityChart = () => {
    if (!result?.equity_curve || result.equity_curve.length === 0) return null

    const data = result.equity_curve
    const width = 600
    const height = 300
    const padding = 20
    const maxVal = Math.max(...data)
    const minVal = Math.min(...data)
    const range = maxVal - minVal || 1

    const points = data.map((val, i) => {
      const x = padding + (i / (data.length - 1)) * (width - 2 * padding)
      const y = height - padding - ((val - minVal) / range) * (height - 2 * padding)
      return `${x},${y}`
    }).join(' ')

    return (
      <div style={{ marginTop: '20px' }}>
        <h3>Equity Curve</h3>
        <svg width={width} height={height} style={{ border: '1px solid #ccc' }}>
          <polyline
            fill="none"
            stroke="#2563eb"
            strokeWidth="2"
            points={points}
          />
        </svg>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Crypto Backtester</h1>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label>
            CSV File:
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              required
              style={{ marginLeft: '10px' }}
            />
          </label>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
          <div>
            <label>
              Gaussian Period:
              <input
                type="number"
                name="gaussian_period"
                value={formData.gaussian_period}
                onChange={handleInputChange}
                style={{ marginLeft: '10px', width: '100%' }}
              />
            </label>
          </div>
          <div>
            <label>
              Gaussian Multiplier:
              <input
                type="number"
                name="gaussian_multiplier"
                value={formData.gaussian_multiplier}
                onChange={handleInputChange}
                step="0.1"
                style={{ marginLeft: '10px', width: '100%' }}
              />
            </label>
          </div>
          <div>
            <label>
              Slope Lookback:
              <input
                type="number"
                name="slope_lookback"
                value={formData.slope_lookback}
                onChange={handleInputChange}
                style={{ marginLeft: '10px', width: '100%' }}
              />
            </label>
          </div>
          <div>
            <label>
              Donchian Period:
              <input
                type="number"
                name="donchian_period"
                value={formData.donchian_period}
                onChange={handleInputChange}
                style={{ marginLeft: '10px', width: '100%' }}
              />
            </label>
          </div>
          <div>
            <label>
              Position Size %:
              <input
                type="number"
                name="position_size_percent"
                value={formData.position_size_percent}
                onChange={handleInputChange}
                step="0.1"
                style={{ marginLeft: '10px', width: '100%' }}
              />
            </label>
          </div>
          <div>
            <label>
              Initial Capital:
              <input
                type="number"
                name="initial_capital"
                value={formData.initial_capital}
                onChange={handleInputChange}
                step="100"
                style={{ marginLeft: '10px', width: '100%' }}
              />
            </label>
          </div>
          <div>
            <label>
              Direction:
              <select
                name="direction"
                value={formData.direction}
                onChange={handleInputChange}
                style={{ marginLeft: '10px', width: '100%' }}
              >
                <option value="both">Both</option>
                <option value="long_only">Long Only</option>
                <option value="short_only">Short Only</option>
              </select>
            </label>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={!file || loading}
          style={{ marginTop: '20px', padding: '10px 20px' }}
        >
          {loading ? 'Running...' : 'Run Backtest'}
        </button>
      </form>

      {error && (
        <div style={{ color: 'red', marginBottom: '20px' }}>
          Error: {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h2>Results</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '10px' }}>
            <div>
              <strong>Sharpe Ratio:</strong>
              <div>{result.sharpe?.toFixed(2) || 'N/A'}</div>
            </div>
            <div>
              <strong>Max Drawdown:</strong>
              <div>{result.max_drawdown?.toFixed(2) || 'N/A'}%</div>
            </div>
            <div>
              <strong>Win Rate:</strong>
              <div>{result.win_rate?.toFixed(2) || 'N/A'}%</div>
            </div>
            <div>
              <strong>Total Return:</strong>
              <div>{result.total_return?.toFixed(2) || 'N/A'}%</div>
            </div>
            <div>
              <strong>Trade Count:</strong>
              <div>{result.trade_count || 0}</div>
            </div>
          </div>

          {renderEquityChart()}
        </div>
      )}
    </div>
  )
}

export default App

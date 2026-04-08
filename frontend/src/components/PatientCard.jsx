function PatientCard({ observation, stepCount }) {
  if (!observation) return null

  const { patient_info, vitals, symptoms, physical_exam_findings, lab_results } = observation

  const getVitalColor = (type, value) => {
    // Simple vital sign evaluation
    if (type === 'heart_rate') {
      if (value < 60 || value > 100) return 'text-warning'
      return 'text-success'
    }
    if (type === 'temperature') {
      if (value > 38.0) return 'text-danger'
      return 'text-success'
    }
    if (type === 'oxygen_saturation') {
      if (value < 94) return 'text-danger'
      return 'text-success'
    }
    return 'text-white'
  }

  return (
    <div className="card-medical">
      {/* Patient Header */}
      <div className="flex justify-between items-start pb-4 border-b border-white/10">
        <div>
          <h2 className="text-2xl font-bold text-white">{patient_info.name}</h2>
          <p className="text-gray-400">{patient_info.age} y/o • {patient_info.gender}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-400">Step {stepCount}</p>
          <p className="text-lg font-semibold text-medical">{observation.task_name}</p>
        </div>
      </div>

      {/* Chief Complaint */}
      <div>
        <h3 className="text-sm font-semibold text-gray-300 mb-2">PRESENTING COMPLAINT</h3>
        <p className="text-white">{patient_info.presenting_complaint}</p>
      </div>

      {/* Vitals Grid */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <div className="glass-dark p-3 rounded-lg text-center">
          <p className="text-xs text-gray-400">HR</p>
          <p className={`text-lg font-bold ${getVitalColor('heart_rate', vitals.heart_rate)}`}>
            {vitals.heart_rate}
          </p>
          <p className="text-xs text-gray-400">bpm</p>
        </div>
        <div className="glass-dark p-3 rounded-lg text-center">
          <p className="text-xs text-gray-400">BP</p>
          <p className="text-lg font-bold text-white">{vitals.blood_pressure}</p>
          <p className="text-xs text-gray-400">mmHg</p>
        </div>
        <div className="glass-dark p-3 rounded-lg text-center">
          <p className="text-xs text-gray-400">Temp</p>
          <p className={`text-lg font-bold ${getVitalColor('temperature', vitals.temperature)}`}>
            {vitals.temperature.toFixed(1)}
          </p>
          <p className="text-xs text-gray-400">°C</p>
        </div>
        <div className="glass-dark p-3 rounded-lg text-center">
          <p className="text-xs text-gray-400">RR</p>
          <p className="text-lg font-bold text-white">{vitals.respiratory_rate}</p>
          <p className="text-xs text-gray-400">/min</p>
        </div>
        <div className="glass-dark p-3 rounded-lg text-center">
          <p className="text-xs text-gray-400">O₂</p>
          <p className={`text-lg font-bold ${getVitalColor('oxygen_saturation', vitals.oxygen_saturation)}`}>
            {vitals.oxygen_saturation.toFixed(1)}
          </p>
          <p className="text-xs text-gray-400">%</p>
        </div>
      </div>

      {/* Symptoms */}
      <div>
        <h3 className="text-sm font-semibold text-gray-300 mb-2">SYMPTOMS</h3>
        <div className="flex flex-wrap gap-2">
          {symptoms.map((symptom, idx) => (
            <span key={idx} className="px-3 py-1 bg-warning/20 text-warning rounded-full text-sm border border-warning/30">
              {symptom}
            </span>
          ))}
        </div>
      </div>

      {/* Physical Examination */}
      <div>
        <h3 className="text-sm font-semibold text-gray-300 mb-2">PHYSICAL EXAMINATION</h3>
        <div className="space-y-1">
          {Object.entries(physical_exam_findings).map(([key, value]) => (
            <div key={key} className="flex justify-between text-sm">
              <span className="text-gray-400 capitalize">{key.replace(/_/g, ' ')}:</span>
              <span className="text-white">{value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Lab Results */}
      {lab_results && Object.keys(lab_results).length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-300 mb-2">LAB RESULTS</h3>
          <div className="space-y-1">
            {Object.entries(lab_results).map(([key, value]) => (
              <div key={key} className="flex justify-between text-sm p-2 bg-medical/10 rounded border border-medical/20">
                <span className="text-gray-300 capitalize">{key.replace(/_/g, ' ')}:</span>
                <span className="text-medical font-semibold">{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Medical History & Allergies */}
      <div className="grid grid-cols-2 gap-4 p-3 bg-danger/5 rounded-lg border border-danger/20">
        <div>
          <p className="text-xs font-semibold text-gray-400 mb-1">MEDICAL HISTORY</p>
          <p className="text-sm text-white">{patient_info.medical_history.join(', ') || 'None'}</p>
        </div>
        <div>
          <p className="text-xs font-semibold text-gray-400 mb-1">ALLERGIES</p>
          <p className="text-sm text-danger">{patient_info.allergies.join(', ') || 'NKDA'}</p>
        </div>
      </div>
    </div>
  )
}

export default PatientCard

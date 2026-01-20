import React, { useState, useRef, useEffect } from 'react';
import { 
  Leaf, Bike, Recycle, Droplets, Zap, Award, TrendingUp, 
  MapPin, Users, Calendar, Star, ChevronDown, ChevronUp,
  Camera, Video, Map, Upload, Shield, CheckCircle, AlertTriangle,
  Clock, School, Settings, Plus, Trash2, UserCheck, UserX,
  Eye, EyeOff, Key, LogOut
} from 'lucide-react';

const App = () => {
  // Admin state
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const adminPasscode = "green2025"; // Change this to your desired password
  
  // Existing state from your original app
  const [selectedAction, setSelectedAction] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [userSchool, setUserSchool] = useState('Lincoln High School');
  const [evidenceType, setEvidenceType] = useState('photo');
  const [evidenceFile, setEvidenceFile] = useState(null);
  const [evidencePreview, setEvidencePreview] = useState(null);
  const [locationCheckIn, setLocationCheckIn] = useState(false);
  const [gpsLocation, setGpsLocation] = useState(null);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [submittedActions, setSubmittedActions] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef(null);

  // Schools management
  const [approvedSchools, setApprovedSchools] = useState([
    'Lincoln High School', 
    'Washington Academy', 
    'Roosevelt College Prep', 
    'Jefferson STEM School', 
    'Adams Environmental Institute'
  ]);
  const [pendingSchools, setPendingSchools] = useState([]);
  const [newSchoolName, setNewSchoolName] = useState('');

  // Competition management
  const [currentCompetition, setCurrentCompetition] = useState({
    name: "Fall 2025 Eco Challenge",
    startDate: "2025-09-01",
    endDate: "2025-12-15",
    isActive: true
  });
  const [competitionName, setCompetitionName] = useState('');
  const [competitionStart, setCompetitionStart] = useState('');
  const [competitionEnd, setCompetitionEnd] = useState('');

  // Existing eco-actions and leaderboard data
  const ecoActions = [
    { id: 'biking', name: 'Biking to School', icon: Bike, co2Savings: 0.8, points: 15, requiresLocation: true, evidenceTypes: ['photo', 'video'] },
    { id: 'recycling', name: 'Proper Recycling', icon: Recycle, co2Savings: 0.3, points: 8, requiresLocation: false, evidenceTypes: ['photo', 'video'] },
    { id: 'water', name: 'Water Conservation Challenge', icon: Droplets, co2Savings: 0.2, points: 6, requiresLocation: true, evidenceTypes: ['photo', 'video'] },
    { id: 'cleanup', name: 'Campus Clean-up', icon: Leaf, co2Savings: 0.5, points: 20, requiresLocation: true, evidenceTypes: ['photo', 'video'] },
    { id: 'energy', name: 'Energy Saving Initiative', icon: Zap, co2Savings: 0.4, points: 12, requiresLocation: true, evidenceTypes: ['photo', 'video'] }
  ];

  const [impactStats, setImpactStats] = useState({
    totalActions: 2156,
    totalCO2Saved: 1247.3,
    totalPoints: 24568,
    activeStudents: 847,
    verifiedActions: 1982
  });

  const [leaderboard, setLeaderboard] = useState([
    { id: 1, name: 'Lincoln High School', points: 8420, actions: 623, students: 187, trend: 'up' },
    { id: 2, name: 'Jefferson STEM School', points: 7890, actions: 598, students: 156, trend: 'up' },
    { id: 3, name: 'Washington Academy', points: 6234, actions: 487, students: 203, trend: 'down' },
    { id: 4, name: 'Roosevelt College Prep', points: 5678, actions: 432, students: 142, trend: 'up' },
    { id: 5, name: 'Adams Environmental Institute', points: 4320, actions: 321, students: 98, trend: 'down' }
  ]);

  // Admin functions
  const handleAdminLogin = (e) => {
    e.preventDefault();
    if (adminPassword === adminPasscode) {
      setIsAdmin(true);
      setAdminPassword('');
    }
  };

  const handleAdminLogout = () => {
    setIsAdmin(false);
  };

  const addSchoolRequest = (e) => {
    e.preventDefault();
    if (newSchoolName && !pendingSchools.includes(newSchoolName) && !approvedSchools.includes(newSchoolName)) {
      setPendingSchools(prev => [...prev, newSchoolName]);
      setNewSchoolName('');
    }
  };

  const approveSchool = (schoolName) => {
    setApprovedSchools(prev => [...prev, schoolName]);
    setPendingSchools(prev => prev.filter(s => s !== schoolName));
    setLeaderboard(prev => [...prev, {
      id: prev.length + 1,
      name: schoolName,
      points: 0,
      actions: 0,
      students: 0,
      trend: 'neutral'
    }]);
  };

  const rejectSchool = (schoolName) => {
    setPendingSchools(prev => prev.filter(s => s !== schoolName));
  };

  const createNewCompetition = (e) => {
    e.preventDefault();
    if (competitionName && competitionStart && competitionEnd) {
      // Reset all data for new competition
      setSubmittedActions([]);
      setImpactStats({
        totalActions: 0,
        totalCO2Saved: 0,
        totalPoints: 0,
        activeStudents: 0,
        verifiedActions: 0
      });
      setLeaderboard(approvedSchools.map((school, index) => ({
        id: index + 1,
        name: school,
        points: 0,
        actions: 0,
        students: 0,
        trend: 'neutral'
      })));
      
      setCurrentCompetition({
        name: competitionName,
        startDate: competitionStart,
        endDate: competitionEnd,
        isActive: true
      });
      
      setCompetitionName('');
      setCompetitionStart('');
      setCompetitionEnd('');
    }
  };

  const resetAllData = () => {
    if (window.confirm('Are you sure you want to reset ALL competition data? This cannot be undone.')) {
      setSubmittedActions([]);
      setImpactStats({
        totalActions: 0,
        totalCO2Saved: 0,
        totalPoints: 0,
        activeStudents: 0,
        verifiedActions: 0
      });
      setLeaderboard(approvedSchools.map((school, index) => ({
        id: index + 1,
        name: school,
        points: 0,
        actions: 0,
        students: 0,
        trend: 'neutral'
      })));
    }
  };

  // ... (keep all your existing functions: handleFileUpload, handleLocationCheckIn, simulateAIVerification, handleSubmitAction, getActionIcon)
  
  // Include all your existing functions here (I'm keeping them brief for space)
  const handleFileUpload = (e) => {
  const file = e.target.files[0];
  if (file) {
    // Check file size based on type
    const maxSizePhoto = 5 * 1024 * 1024; // 5MB for photos
    const maxSizeVideo = 50 * 1024 * 1024; // 50MB for videos
    const maxSize = evidenceType === 'photo' ? maxSizePhoto : maxSizeVideo;
    
    if (file.size > maxSize) {
      const maxSizeMB = maxSize / (1024 * 1024);
      const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
      alert(`File too large! Maximum size is ${maxSizeMB}MB. Your file is ${fileSizeMB}MB.`);
      // Clear the file input
      e.target.value = '';
      return;
    }
    
    // Check file type
    const validPhotoTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    const validVideoTypes = ['video/mp4', 'video/webm', 'video/ogg'];
    const validTypes = evidenceType === 'photo' ? validPhotoTypes : validVideoTypes;
    
    if (!validTypes.includes(file.type)) {
      alert(`Invalid file type! Please upload ${evidenceType === 'photo' ? 'an image' : 'a video'} file.`);
      e.target.value = '';
      return;
    }
    
    setEvidenceFile(file);
    const reader = new FileReader();
    reader.onload = (e) => setEvidencePreview(e.target.result);
    reader.readAsDataURL(file);
  }
};

  const handleLocationCheckIn = () => {
  setIsProcessing(true);
  
  // Step 1: Check if browser supports Geolocation
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by your browser');
    setIsProcessing(false);
    return;
  }
  
  // Step 2: Request real location from browser
  navigator.geolocation.getCurrentPosition(
    // Success callback - location found!
    (position) => {
      setGpsLocation({
        lat: position.coords.latitude.toFixed(4),
        lng: position.coords.longitude.toFixed(4)
      });
      setIsProcessing(false);
    },
    // Error callback - something went wrong
    (error) => {
      alert('Error getting location: ' + error.message);
      setIsProcessing(false);
    },
    // Options for location request
    {
      enableHighAccuracy: true,  // Use GPS if available (more accurate)
      timeout: 10000,             // Wait max 10 seconds
      maximumAge: 0               // Don't use cached location
    }
  );
};

  const simulateAIVerification = () => Math.random() > 0.1;

  const handleSubmitAction = (e) => {
    e.preventDefault();
    if (!selectedAction || quantity <= 0 || !evidenceFile) return;
    const action = ecoActions.find(a => a.id === selectedAction);
    if (action && (!action.requiresLocation || gpsLocation)) {
      setIsProcessing(true);
      setTimeout(() => {
        const isVerified = simulateAIVerification();
        const newAction = {
          id: Date.now(),
          action: selectedAction,
          quantity: parseInt(quantity),
          school: userSchool,
          points: action.points * quantity,
          co2Saved: action.co2Savings * quantity,
          timestamp: new Date().toLocaleDateString(),
          evidenceType: evidenceType,
          evidenceVerified: isVerified,
          locationCheckIn: gpsLocation || null
        };
        setSubmittedActions(prev => [newAction, ...prev.slice(0, 4)]);
        setImpactStats(prev => ({
          totalActions: prev.totalActions + newAction.quantity,
          totalCO2Saved: prev.totalCO2Saved + newAction.co2Saved,
          totalPoints: prev.totalPoints + newAction.points,
          activeStudents: isVerified ? prev.activeStudents + 1 : prev.activeStudents,
          verifiedActions: isVerified ? prev.verifiedActions + newAction.quantity : prev.verifiedActions
        }));
        if (isVerified) {
          setLeaderboard(prev => prev.map(item => 
            item.name === userSchool 
              ? { ...item, points: item.points + newAction.points, actions: item.actions + newAction.quantity, students: item.students + 1 }
              : item
          ).sort((a, b) => b.points - a.points));
        }
        setSelectedAction('');
        setQuantity(1);
        setEvidenceFile(null);
        setEvidencePreview(null);
        setLocationCheckIn(false);
        setGpsLocation(null);
        setIsProcessing(false);
      }, 2000);
    }
  };

  const getActionIcon = (actionId) => {
    const action = ecoActions.find(a => a.id === actionId);
    return action ? action.icon : Leaf;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-green-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-green-600 p-2 rounded-lg">
                <Leaf className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">School Green Impact Tracker</h1>
                <p className="text-green-600">Eco-challenges for schools & students</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {!isAdmin ? (
               <button 
                  onClick={() => setShowLeaderboard(!showLeaderboard)}
                  aria-label={showLeaderboard ? 'Hide school leaderboard' : 'Show school leaderboard'}
                  aria-expanded={showLeaderboard}
                >
                  {showLeaderboard ? <ChevronUp className="h-4 w-4" aria-hidden="true" /> : <ChevronDown className="h-4 w-4" aria-hidden="true" />}
                  <span>{showLeaderboard ? 'Hide' : 'View'} School Rankings</span>
              </button>
              ) : (
                <div className="flex items-center space-x-2 bg-red-100 text-red-800 px-3 py-2 rounded-lg">
                  <Settings className="h-4 w-4" />
                  <span>Admin Mode</span>
                  <button
                    onClick={handleAdminLogout}
                    className="ml-2 text-red-600 hover:text-red-800"
                  >
                    <LogOut className="h-4 w-4" />
                  </button>
                </div>
              )}
              
              {/* Admin Login Button (only visible when not admin) */}
              {!isAdmin && (
                <div className="relative group">
                  <button className="bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700">
                    <Key className="h-4 w-4" />
                  </button>
                  {/* Admin Login Form (popup) */}
                  <div className="absolute right-0 mt-2 w-64 bg-white shadow-lg rounded-lg p-4 z-50 hidden group-hover:block">
                    <form onSubmit={handleAdminLogin} className="space-y-3">
                      <h3 className="font-medium text-gray-900">Admin Login</h3>
                      <input
                        type="password"
                        value={adminPassword}
                        onChange={(e) => setAdminPassword(e.target.value)}
                        placeholder="Enter admin password"
                        className="w-full p-2 border border-gray-300 rounded"
                        required
                      />
                      <button
                        type="submit"
                        className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
                      >
                        Login
                      </button>
                    </form>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Competition Info Banner */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-bold text-blue-900">{currentCompetition.name}</h2>
              <p className="text-blue-700 text-sm">
                {currentCompetition.startDate} to {currentCompetition.endDate} • 
                {currentCompetition.isActive ? ' 🟢 Active' : ' 🔴 Inactive'}
              </p>
            </div>
            {isAdmin && (
              <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                Admin Controls Available
              </span>
            )}
          </div>
        </div>

        {/* Admin Dashboard (only visible when admin) */}
        {isAdmin && (
          <div className="bg-white rounded-xl p-6 shadow-sm border border-purple-200 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <Settings className="h-6 w-6 text-purple-600 mr-2" />
              Admin Dashboard
            </h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* School Management */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="font-bold text-lg mb-4 flex items-center">
                  <School className="h-5 w-5 text-blue-600 mr-2" />
                  School Management
                </h3>
                
                {/* Add New School */}
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Add New School</h4>
                  <form onSubmit={addSchoolRequest} className="flex space-x-2">
                    <input
                      type="text"
                      value={newSchoolName}
                      onChange={(e) => setNewSchoolName(e.target.value)}
                      placeholder="Enter school name"
                      className="flex-1 p-2 border border-gray-300 rounded"
                    />
                    <button
                      type="submit"
                      className="bg-green-600 text-white p-2 rounded hover:bg-green-700"
                    >
                      <Plus className="h-4 w-4" />
                    </button>
                  </form>
                </div>
                
                {/* Pending Schools */}
                {pendingSchools.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">Pending Approvals ({pendingSchools.length})</h4>
                    <div className="space-y-2">
                      {pendingSchools.map((school, index) => (
                        <div key={index} className="flex items-center justify-between p-2 bg-yellow-50 rounded">
                          <span className="text-yellow-800">{school}</span>
                          <div className="flex space-x-1">
                            <button
                              onClick={() => approveSchool(school)}
                              className="bg-green-100 text-green-700 p-1 rounded hover:bg-green-200"
                            >
                              <UserCheck className="h-4 w-4" />
                            </button>
                            <button
                              onClick={() => rejectSchool(school)}
                              className="bg-red-100 text-red-700 p-1 rounded hover:bg-red-200"
                            >
                              <UserX className="h-4 w-4" />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Approved Schools */}
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Approved Schools ({approvedSchools.length})</h4>
                  <div className="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto">
                    {approvedSchools.map((school, index) => (
                      <div key={index} className="text-sm bg-green-50 text-green-800 p-2 rounded">
                        {school}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              
              {/* Competition Management */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="font-bold text-lg mb-4 flex items-center">
                  <Award className="h-5 w-5 text-orange-600 mr-2" />
                  Competition Management
                </h3>
                
                {/* Create New Competition */}
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Start New Competition</h4>
                  <form onSubmit={createNewCompetition} className="space-y-2">
                    <input
                      type="text"
                      value={competitionName}
                      onChange={(e) => setCompetitionName(e.target.value)}
                      placeholder="Competition name"
                      className="w-full p-2 border border-gray-300 rounded"
                      required
                    />
                    <div className="grid grid-cols-2 gap-2">
                      <input
                        type="date"
                        value={competitionStart}
                        onChange={(e) => setCompetitionStart(e.target.value)}
                        className="p-2 border border-gray-300 rounded"
                        required
                      />
                      <input
                        type="date"
                        value={competitionEnd}
                        onChange={(e) => setCompetitionEnd(e.target.value)}
                        className="p-2 border border-gray-300 rounded"
                        required
                      />
                    </div>
                    <button
                      type="submit"
                      className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-700"
                    >
                      Launch New Competition
                    </button>
                  </form>
                </div>
                
                {/* Reset Controls */}
                <div className="bg-red-50 p-4 rounded-lg">
                  <h4 className="font-medium text-red-800 mb-2">Emergency Reset</h4>
                  <p className="text-red-700 text-sm mb-2">Reset all competition data (use carefully!)</p>
                  <button
                    onClick={resetAllData}
                    className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700 flex items-center justify-center space-x-2"
                  >
                    <Trash2 className="h-4 w-4" />
                    <span>Reset All Data</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Rest of your existing UI components go here */}
        {/* Impact Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          {/* ... your existing impact stats code ... */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Actions</p>
                <p className="text-3xl font-bold text-gray-900">{impactStats.totalActions.toLocaleString()}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">CO2 Saved (tons)</p>
                <p className="text-3xl font-bold text-gray-900">{impactStats.totalCO2Saved.toLocaleString()}</p>
              </div>
              <Leaf className="h-8 w-8 text-green-600" />
            </div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Verified Actions</p>
                <p className="text-3xl font-bold text-gray-900">{impactStats.verifiedActions.toLocaleString()}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Students</p>
                <p className="text-3xl font-bold text-gray-900">{impactStats.activeStudents.toLocaleString()}</p>
              </div>
              <Users className="h-8 w-8 text-green-600" />
            </div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">School Points</p>
                <p className="text-3xl font-bold text-gray-900">{impactStats.totalPoints.toLocaleString()}</p>
              </div>
              <Award className="h-8 w-8 text-green-600" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Action Submission Form */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Log Your Eco-Action</h2>
            <form onSubmit={handleSubmitAction} className="space-y-6">
              <div>
                <label htmlFor="eco-action-select" className="block text-sm font-medium text-gray-700 mb-2">
                    Eco-Action
                  </label>
                  <select 
                    id="eco-action-select"
                    value={selectedAction} 
                    onChange={...}
                    aria-required="true"
                    aria-describedby="eco-action-help"
                  >
                    <option value="">Select an eco-action</option>
                    ...
                  </select>
                  <p id="eco-action-help" className="sr-only">
                    Choose an environmental action to log. You'll earn points and save CO2.
                  </p>
                    setSelectedAction(e.target.value);
                    const action = ecoActions.find(a => a.id === e.target.value);
                    if (action && action.requiresLocation) {
                      setLocationCheckIn(true);
                    }
                  }}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="">Select an eco-action</option>
                  {ecoActions.map(action => (
                    <option key={action.id} value={action.id}>
                      {action.name} (+{action.points} pts, {action.co2Savings} tons CO2)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">School</label>
                <select
                  value={userSchool}
                  onChange={(e) => setUserSchool(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  disabled={isAdmin} // Admin can't submit actions
                >
                  {approvedSchools.map(school => (
                    <option key={school} value={school}>
                      {school}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Quantity</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  disabled={isAdmin}
                />
              </div>

              {selectedAction && !isAdmin && (
                <>
                  <div className="border-2 border-dashed border-green-200 rounded-lg p-4">
                    <label className="block text-sm font-medium text-gray-700 mb-3">Evidence Upload</label>
                    <div className="flex space-x-4 mb-3">
                      <button
                        type="button"
                        onClick={() => setEvidenceType('photo')}
                        className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
                          evidenceType === 'photo' 
                            ? 'bg-green-100 text-green-700 border border-green-300' 
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        <Camera className="h-4 w-4" />
                        <span>Photo</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => setEvidenceType('video')}
                        className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
                          evidenceType === 'video' 
                            ? 'bg-green-100 text-green-700 border border-green-300' 
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        <Video className="h-4 w-4" />
                        <span>Video</span>
                      </button>
                    </div>
                    
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept={evidenceType === 'photo' ? 'image/*' : 'video/*'}
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="w-full flex items-center justify-center space-x-2 bg-green-50 text-green-700 py-3 px-4 rounded-lg border border-green-200 hover:bg-green-100 transition-colors"
                    >
                      <Upload className="h-5 w-5" />
                      <span>Upload {evidenceType === 'photo' ? 'Photo' : 'Video'}</span>
                    </button>
                    
                    {evidencePreview && (
                      <div className="mt-3">
                        {evidenceType === 'photo' ? (
                          <img 
                            src={evidencePreview} 
                            alt="Evidence preview" 
                            className="max-h-32 rounded-lg object-cover"
                          />
                        ) : (
                          <video 
                            src={evidencePreview} 
                            className="max-h-32 rounded-lg"
                            controls
                          />
                        )}
                      </div>
                    )}
                  </div>

                  {ecoActions.find(a => a.id === selectedAction)?.requiresLocation && (
                    <div className="border border-green-200 rounded-lg p-4">
                      <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-3">
                        <input
                          type="checkbox"
                          checked={locationCheckIn}
                          onChange={(e) => setLocationCheckIn(e.target.checked)}
                          className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                        />
                        <span>Enable Location Check-in</span>
                        <Map className="h-4 w-4 text-green-600" />
                      </label>
                      
                      {locationCheckIn && (
                        <div className="space-y-3">
                          {!gpsLocation ? (
                            <button
                              type="button"
                              onClick={handleLocationCheckIn}
                              disabled={isProcessing}
                              className="w-full flex items-center justify-center space-x-2 bg-blue-50 text-blue-700 py-2 px-4 rounded-lg border border-blue-200 hover:bg-blue-100 transition-colors disabled:opacity-50"
                            >
                              {isProcessing ? (
                                <Clock className="h-4 w-4 animate-spin" />
                              ) : (
                                <MapPin className="h-4 w-4" />
                              )}
                              <span>{isProcessing ? 'Getting Location...' : 'Check-in Location'}</span>
                            </button>
                          ) : (
                            <div className="bg-green-50 p-3 rounded-lg">
                              <div className="flex items-center space-x-2 mb-1">
                                <CheckCircle className="h-4 w-4 text-green-600" />
                                <span className="text-sm font-medium text-green-700">Location Verified</span>
                              </div>
                              <p className="text-xs text-gray-600">
                                {gpsLocation.lat}, {gpsLocation.lng}
                              </p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </>
              )}

              {!isAdmin && (
                <button
                  type="submit"
                  disabled={
                    !selectedAction || 
                    quantity <= 0 || 
                    !evidenceFile || 
                    (ecoActions.find(a => a.id === selectedAction)?.requiresLocation && !gpsLocation) ||
                    isProcessing
                  }
                  className="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium flex items-center justify-center space-x-2"
                >
                  {isProcessing ? (
                    <>
                      <Clock className="h-5 w-5 animate-spin" />
                      <span>Processing with AI...</span>
                    </>
                  ) : (
                    <>
                      <Shield className="h-5 w-5" />
                      <span>Submit for Verification</span>
                    </>
                  )}
                </button>
              )}
            </form>
          </div>

          {/* Recent Actions */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Submissions</h2>
            <div className="space-y-4">
              {submittedActions.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No actions logged yet. Start making an impact!</p>
              ) : (
                submittedActions.map(action => {
                  const ActionIcon = getActionIcon(action.action);
                  const actionData = ecoActions.find(a => a.id === action.action);
                  return (
                    <div key={action.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <div className={`p-2 rounded-lg ${
                          action.evidenceVerified ? 'bg-green-100' : 'bg-yellow-100'
                        }`}>
                          <ActionIcon className={`h-5 w-5 ${
                            action.evidenceVerified ? 'text-green-600' : 'text-yellow-600'
                          }`} />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-1">
                            <p className="font-medium text-gray-900">{actionData?.name}</p>
                            <span className={`text-xs px-2 py-1 rounded-full ${
                              action.evidenceVerified 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {action.evidenceVerified ? 'Verified' : 'Under Review'}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">
                            {action.school} • {action.quantity}x • {action.timestamp}
                          </p>
                          <div className="flex items-center space-x-4 text-xs text-gray-500">
                            <span>+{action.points} points</span>
                            <span>{action.co2Saved} tons CO2</span>
                            {action.locationCheckIn && (
                              <span className="flex items-center space-x-1">
                                <MapPin className="h-3 w-3" />
                                <span>Location verified</span>
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* Leaderboard */}
        {showLeaderboard && !isAdmin && (
          <div className="mt-8 bg-white rounded-xl p-6 shadow-sm border border-green-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <School className="h-6 w-6 text-blue-500 mr-2" />
              School Competition Leaderboard
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Rank</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">School</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Points</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Actions</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Students</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Trend</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((item, index) => (
                    <tr key={item.id} className="border-b border-gray-100 hover:bg-green-50">
                      <td className="py-4 px-4">
                        <div className="flex items-center">
                          {index === 0 && <Star className="h-5 w-5 text-yellow-500 mr-2" />}
                          {index === 1 && <Star className="h-5 w-5 text-gray-400 mr-2" />}
                          {index === 2 && <Star className="h-5 w-5 text-amber-600 mr-2" />}
                          <span className={`font-bold ${index < 3 ? 'text-green-600' : 'text-gray-900'}`}>
                            #{item.id}
                          </span>
                        </div>
                      </td>
                      <td className="py-4 px-4 font-medium text-gray-900">
                        <div className="flex items-center">
                          <School className="h-4 w-4 text-blue-600 mr-2" />
                          {item.name}
                        </div>
                      </td>
                      <td className="py-4 px-4 font-bold text-green-600">{item.points.toLocaleString()}</td>
                      <td className="py-4 px-4 text-gray-600">{item.actions.toLocaleString()}</td>
                      <td className="py-4 px-4">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm">
                          {item.students} students
                        </span>
                      </td>
                      <td className="py-4 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          item.trend === 'up' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {item.trend === 'up' ? '↗ Rising' : '↘ Declining'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* How it Works */}
        {!isAdmin && (
          <div className="mt-12 bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl p-8 text-white">
            <h2 className="text-2xl font-bold mb-6">How School Challenges Work</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="bg-white bg-opacity-20 rounded-full p-4 inline-block mb-4">
                  <Camera className="h-8 w-8" />
                </div>
                <h3 className="font-bold text-lg mb-2">Photo/Video Evidence</h3>
                <p className="text-green-100">Upload proof of your eco-actions. Our AI verifies authenticity and flags duplicates.</p>
              </div>
              <div className="text-center">
                <div className="bg-white bg-opacity-20 rounded-full p-4 inline-block mb-4">
                  <Map className="h-8 w-8" />
                </div>
                <h3 className="font-bold text-lg mb-2">Location Verification</h3>
                <p className="text-green-100">Check-in at specific locations to confirm participation in campus events and activities.</p>
              </div>
              <div className="text-center">
                <div className="bg-white bg-opacity-20 rounded-full p-4 inline-block mb-4">
                  <Award className="h-8 w-8" />
                </div>
                <h3 className="font-bold text-lg mb-2">School Competition</h3>
                <p className="text-green-100">Compete with other schools to earn the top spot on our leaderboard and win eco-awards.</p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <Leaf className="h-6 w-6 text-green-400" />
              <span className="text-xl font-bold">School Green Impact Tracker</span>
            </div>
            <p className="text-gray-400">Building environmentally conscious schools through friendly competition and verified actions.</p>
            <p className="text-gray-500 text-sm mt-4">© 2025 School Green Impact Tracker. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;

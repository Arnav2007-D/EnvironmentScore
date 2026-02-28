import React, { useState, useRef, useEffect } from 'react';
import { 
  Leaf, Bike, Recycle, Droplets, Zap, Award, TrendingUp, 
  MapPin, Users, Calendar, Star, ChevronDown, ChevronUp,
  Camera, Video, Map, Upload, Shield, CheckCircle, AlertTriangle,
  Clock, School, Settings, Plus, Trash2, UserCheck, UserX,
  Eye, EyeOff, Key, LogOut, MessageCircle, Send
} from 'lucide-react';

const App = () => {
  // Admin state
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const [showAdminForm, setShowAdminForm] = useState(false);
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

  // Chatbot state
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState([
    { from: 'bot', text: 'Hi! I can help you log eco-actions and understand the competition. What would you like to know?' }
  ]);

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
      setShowAdminForm(false);
    } else {
      alert('Incorrect password');
    }
  };

  const handleAdminLogout = () => {
    setIsAdmin(false);
    setShowAdminForm(false);
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
          ).sort((a, b) => b.points - a.points).map((item, index) => ({ ...item, id: index + 1 })));
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

  // Basic chatbot logic (very simple rules)
  const getBotReply = (message) => {
    const text = message.toLowerCase();

    // Help with logging actions
    if (text.includes('how') && text.includes('log')) {
      return 'To log an eco-action: choose an action from the dropdown, pick your school, set the quantity, upload a photo or video, and then submit for verification.';
    }

    // Explain points
    if (text.includes('points') || text.includes('score')) {
      return 'Each eco-action has a points value. When your action is verified, those points are added to your school on the leaderboard.';
    }

    // Explain CO2
    if (text.includes('co2') || text.includes('carbon')) {
      return 'Each action shows an estimated CO₂ saving. When you log actions, we add those savings to the total CO₂ saved across all students.';
    }

    // Leaderboard / competition
    if (text.includes('leaderboard') || text.includes('rank') || text.includes('competition')) {
      return `Right now the competition is "${currentCompetition.name}" from ${currentCompetition.startDate} to ${currentCompetition.endDate}. Schools earn points when students submit verified eco-actions.`;
    }

    // Ask about specific eco-action
    const bikingAction = ecoActions.find(a => a.id === 'biking');
    if (text.includes('bike') || text.includes('biking')) {
      return `Biking to school gives you ${bikingAction.points} points per action and saves about ${bikingAction.co2Savings} tons of CO₂ for each logged ride.`;
    }

    // Fallback
    return 'I am a simple helper bot. Try asking about: how to log an action, how points work, CO₂ savings, or the school leaderboard.';
  };

  const handleSendChatMessage = (e) => {
    e.preventDefault();
    const trimmed = chatInput.trim();
    if (!trimmed) return;

    const reply = getBotReply(trimmed);

    setChatMessages((prev) => [
      ...prev,
      { from: 'user', text: trimmed },
      { from: 'bot', text: reply }
    ]);

    setChatInput('');
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
                  className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
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
                    aria-label="Log out of admin mode"
                  >
                    <LogOut className="h-4 w-4" />
                  </button>
                </div>
              )}
              
              {/* Admin Login Button (only visible when not admin) */}
              {!isAdmin && (
                <div className="relative">
                  <button 
                    onClick={() => setShowAdminForm(!showAdminForm)}
                    className="bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700"
                    aria-label="Admin login"
                  >
                    <Key className="h-4 w-4" />
                  </button>
                  {/* Admin Login Form (popup) */}
                  {showAdminForm && (
                    <div className="absolute right-0 mt-2 w-64 bg-white shadow-lg rounded-lg p-4 z-50 border border-gray-200">
                      <form onSubmit={handleAdminLogin} className="space-y-3">
                        <h3 className="font-medium text-gray-900">Admin Login</h3>
                        <input
                          type="password"
                          value={adminPassword}
                          onChange={(e) => setAdminPassword(e.target.value)}
                          placeholder="Enter admin password"
                          className="w-full p-2 border border-gray-300 rounded"
                          required
                          autoFocus
                        />
                        <button
                          type="submit"
                          className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
                        >
                          Login
                        </button>
                        <button
                          type="button"
                          onClick={() => setShowAdminForm(false)}
                          className="w-full bg-gray-200 text-gray-700 py-2 rounded hover:bg-gray-300"
                        >
                          Cancel
                        </button>
                      </form>
                    </div>
                  )}
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
                      aria-label="Add new school"
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
                              aria-label={`Approve ${school}`}
                            >
                              <UserCheck className="h-4 w-4" />
                            </button>
                            <button
                              onClick={() => rejectSchool(school)}
                              className="bg-red-100 text-red-700 p-1 rounded hover:bg-red-200"
                              aria-label={`Reject ${school}`}
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

        {/* Impact Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
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
                  onChange={(e) => {
                    setSelectedAction(e.target.value);
                    const action = ecoActions.find(a => a.id === e.target.value);
                    if (action && action.requiresLocation) {
                      setLocationCheckIn(true);
                    } else {
                      setLocationCheckIn(false);
                      setGpsLocation(null);
                    }
                  }}
                  aria-required="true"
                  aria-describedby="eco-action-help"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  disabled={isAdmin}
                >
                  <option value="">Select an eco-action</option>
                  {ecoActions.map(action => (
                    <option key={action.id} value={action.id}>
                      {action.name} (+{action.points} pts, {action.co2Savings} tons CO2)
                    </option>
                  ))}
                </select>
                <p id="eco-action-help" className="sr-only">
                  Choose an environmental action to log. You'll earn points and save CO2.
                </p>
              </div>

              <div>
                <label htmlFor="school-select" className="block text-sm font-medium text-gray-700 mb-2">School</label>
                <select
                  id="school-select"
                  value={userSchool}
                  onChange={(e) => setUserSchool(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  disabled={isAdmin}
                >
                  {approvedSchools.map(school => (
                    <option key={school} value={school}>
                      {school}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="quantity-input" className="block text-sm font-medium text-gray-700 mb-2">Quantity</label>
                <input
                  id="quantity-input"
                  type="number"
                  min="1"
                  max="10"
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
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
                        onClick={() => {
                          setEvidenceType('photo');
                          setEvidenceFile(null);
                          setEvidencePreview(null);
                        }}
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
                        onClick={() => {
                          setEvidenceType('video');
                          setEvidenceFile(null);
                          setEvidencePreview(null);
                        }}
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
                      onClick={() => fileInputRef.current

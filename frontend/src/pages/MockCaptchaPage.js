import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MockCaptchaPage.css"; // Import the CSS file for styling
import RecaptchaLogo from "../RecaptchaLogo.svg"; // Correct path to the logo

const MockCaptchaPage = ({ setIsVerified }) => {
  const navigate = useNavigate();
  const [isVerifying, setIsVerifying] = useState(false);
  const [isVerified, setIsVerifiedState] = useState(false);
  const [showCheckmark, setShowCheckmark] = useState(false);

  const handleVerify = () => {
    setIsVerifying(true);
    // Simulate CAPTCHA verification delay
    setTimeout(() => {
      setIsVerifying(false);
      setShowCheckmark(true);
      localStorage.setItem("isVerified", "true");
      setIsVerified(true);
      setTimeout(() => {
        navigate("/home");
      }, 1000); // 1-second delay before redirecting
    }, 2000); // 2-second delay for verification
  };

  return (
    <div className="captcha-container">
      <div className="captcha-box">
        {!isVerifying && !isVerified && (
          <input
            type="checkbox"
            className="captcha-checkbox"
            onChange={handleVerify}
          />
        )}
        <span className="captcha-text">
          {isVerifying ? (
            <div className="spinner"></div>
          ) : showCheckmark ? (
            <div className="checkmark">&#10003;</div>
          ) : (
            "I'm not a robot"
          )}
        </span>
        <img
          src={RecaptchaLogo}
          alt="reCAPTCHA Logo"
          className="captcha-logo"
        />
      </div>
    </div>
  );
};

export default MockCaptchaPage;
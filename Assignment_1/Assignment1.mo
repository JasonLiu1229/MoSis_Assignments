package Assignment1
  model crane_model
  // Types
    type Displacement = Real(unit = "m");
    type Velocity = Real(unit = "m/s");
    type AngularDisplacement = Real(unit = "rad");
    type AngularVelocity = Real(unit = "rad/s");
    type Mass = Real(unit = "kg");
    type length = Real(unit = "m");
    type DampingFactor = Real(unit = "N/(m/s)");
    type gravity = Real(unit = "m/s^2", start = 9.81);

  // Parameters

  // Variables
    
  equation

  end crane_model;
end Assignment1;

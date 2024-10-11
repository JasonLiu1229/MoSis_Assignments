package GantryControlSystem
  model CraneModel
  // Types
    type Meter = Real(unit = "m");
    type Velocity = Real(unit = "m/s");
    type AngularDisplacement = Real(unit = "rad");
    type AngularVelocity = Real(unit = "rad/s");
    type Mass = Real(unit = "kg");
    type DampingFactor = Real(unit = "N/(m/s)");
    type gravity = Real(unit = "m/s^2", start = 9.81);

  // Parameters

  // Variables
  equation

  end CraneModel;
end GantryControlSystem;

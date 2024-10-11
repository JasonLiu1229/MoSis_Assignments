package GantryControlSystem
  model CraneModel
  // Types
    type Meter = Real(unit = "m");
    type Velocity = Real(unit = "m/s");
    type AngularDisplacement = Real(unit = "rad");
    type AngularVelocity = Real(unit = "rad/s");
    type Mass = Real(unit = "kg");
    type DampingFactor = Real(unit = "N/(m/s)");
    type Aceleration = Real(unit = "m/s^2");

  // Parameters
    parameter Meter x "The displacement of the trolley/cart";
    parameter Velocity v "The velocity of the trolley/cart";
    parameter AngularDisplacement theta "The angular displacement of the pendulum";
    parameter AngularVelocity omega "The angular velocity of the pendulum";
    parameter Real u "The control signal to move the pendulum and trolley/cart";
    parameter Mass m "The mass of the pendulum bob/container";
    parameter Mass M "The mass of the trolley/cart";
    parameter Meter r "The length of the rope connecting the trolley/cart and the pendulum bob/container";
    parameter DampingFactor d_p "The damping factor of the pendulum";
    parameter DampingFactor d_c "The damping factor for the motion of the trolley/cart";
    parameter Aceleration g = 9.81 "The acceleration due to gravity";

  // Variables
  equation
    // First equation

    // Second equation

    // Third equation

    // Fourth equation
  end CraneModel;
end GantryControlSystem;

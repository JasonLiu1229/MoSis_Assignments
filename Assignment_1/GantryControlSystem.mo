package GantryControlSystem
  model CraneModel
    type DampingFactor = Real(unit = "N/(m/s)");

  // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2 "The mass of the pendulum bob/container";
    parameter Modelica.Units.SI.Mass M = 10 "The mass of the trolley/cart";
    parameter Modelica.Units.SI.Length r = 1 "The length of the rope connecting the trolley/cart and the pendulum bob/container";
    parameter DampingFactor d_p = 0.5 "The damping factor of the pendulum";
    parameter DampingFactor d_c = 2 "The damping factor for the motion of the trolley/cart";
    constant Modelica.Units.SI.Acceleration g = Modelica.Constants.g_n "The acceleration due to gravity";

  // Variables
    Real u = 0 "The control signal to move the pendulum and trolley/cart";

    Modelica.Units.SI.Length x "The displacement of the trolley/cart";
    Modelica.Units.SI.Velocity v "The velocity of the trolley/cart";

    Modelica.Units.SI.Angle theta "The angular displacement of the pendulum";
    Modelica.Units.SI.AngularVelocity omega "The angular velocity of the pendulum";
  
  initial equation
    x = 0;
    v = 0;
    theta = 0;
    omega = 0;
    
  equation
    // First equation
      der(x) = v;

    // Second equation
      der(theta) = omega;

    // Third equation
      der(v) = (r * (d_c * v - m * (g * sin(theta) * cos(theta) + r * omega^2 * sin(theta)) - u) - (d_p * cos(theta) * omega)) / (-r * (M + m * (sin(theta))^2));

    // Fourth equation
      der(omega) = ((d_p * omega * (m + M)) + (m^2 * r^2 * sin(theta) * cos(theta) * omega^2) + m * r * (((g * sin(theta)) * (m + M)) + (cos(theta) * (u - d_c * v)))) / ((m * r^2) * (-M - (m * (sin(theta))^2)));
  end CraneModel;
end GantryControlSystem;

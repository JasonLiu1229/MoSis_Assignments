package GantryControlSystem
  model CraneModel
  // Parameters
    parameter Modelica.Units.SI.Mass m "The mass of the pendulum bob/container";
    parameter Modelica.Units.SI.Mass M "The mass of the trolley/cart";
    parameter Modelica.Units.SI.Length r "The length of the rope connecting the trolley/cart and the pendulum bob/container";
    parameter Modelica.Units.SI.TranslationalDampingConstant d_p "The damping factor of the pendulum";
    parameter Modelica.Units.SI.TranslationalDampingConstant d_c "The damping factor for the motion of the trolley/cart";
    parameter Modelica.Units.SI.Acceleration g = 9.81 "The acceleration due to gravity";

  // Variables
    Real u "The control signal to move the pendulum and trolley/cart";

    Modelica.Units.SI.Length x "The displacement of the trolley/cart";
    Modelica.Units.SI.Velocity v "The velocity of the trolley/cart";

    Modelica.Units.SI.Angle theta "The angular displacement of the pendulum";
    Modelica.Units.SI.AngularVelocity omega "The angular velocity of the pendulum";
  equation
    // First equation
      der(x) = v;

    // Second equation
      der(theta) = omega;

    // Third equation
      der(v) = (r * (d_c * v - m * (g * sin(theta) * cos(theta) + r * omega^2 * sin(theta)) - u) - (d_p * cos(theta) * omega)) / (-r * (M + m (sin(theta))^2));

    // Fourth equation
  end CraneModel;
end GantryControlSystem;

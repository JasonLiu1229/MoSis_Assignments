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
    Real u "The control signal to move the pendulum and trolley/cart";
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
    der(v) = (r*(d_c*v - m*(g*sin(theta)*cos(theta) + r*omega^2*sin(theta)) - u) - (d_p*cos(theta)*omega))/(-r*(M + m*(sin(theta))^2));
// Fourth equation
    der(omega) = ((d_p*omega*(m + M)) + (m^2*r^2*sin(theta)*cos(theta)*omega^2) + m*r*(((g*sin(theta))*(m + M)) + (cos(theta)*(u - d_c*v))))/((m*r^2)*(-M - (m*(sin(theta))^2)));
// u signal change
    if time < 0.5 then
      u = 1000;
    else
      u = 0;
    end if;
  end CraneModel;

  model CraneModelExpOne
    type DampingFactor = Real(unit = "N/(m/s)");
    // Parameters
    parameter Modelica.Units.SI.Mass M = 10 "The mass of the trolley/cart";
    parameter Modelica.Units.SI.Length r = 1 "The length of the rope connecting the trolley/cart and the pendulum bob/container";
    parameter DampingFactor d_c = 2 "The damping factor for the motion of the trolley/cart";
    constant Modelica.Units.SI.Acceleration g = Modelica.Constants.g_n "The acceleration due to gravity";
    // Variables
    Modelica.Units.SI.Length x "The displacement of the trolley/cart";
    Modelica.Units.SI.Velocity v "The velocity of the trolley/cart";
  initial equation
    x = 0;
    v = 5;
  equation
// First equation
    der(x) = v;
// Second equation
    der(v) = -(d_c/M)*v;
  end CraneModelExpOne;

  model CraneModelExpTwo
    type DampingFactor = Real(unit = "N/(m/s)");
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2 "The mass of the pendulum bob/container";
    parameter Modelica.Units.SI.Length r = 1 "The length of the rope connecting the trolley/cart and the pendulum bob/container";
    parameter DampingFactor d_p = 0.5 "The damping factor of the pendulum";
    constant Modelica.Units.SI.Acceleration g = Modelica.Constants.g_n "The acceleration due to gravity";
    // Variables
    Modelica.Units.SI.Angle theta "The angular displacement of the pendulum";
    Modelica.Units.SI.AngularVelocity omega "The angular velocity of the pendulum";
  initial equation
    theta = 30*Modelica.Constants.pi/180;
    omega = 0;
  equation
    der(theta) = omega;
    der(omega) = -((d_p*omega) + (m*g*r*sin(theta)))/(m*(r^2));
  end CraneModelExpTwo;

  block CraneModelBlock
    extends GantryControlSystem.CraneModel;
    extends Modelica.Blocks.Icons.Block;
    Modelica.Blocks.Interfaces.RealInput u_input "Input signal connector" annotation(
      Placement(transformation(origin = {-40, 0}, extent = {{-84, -12}, {-60, 12}}), iconTransformation(extent = {{-140, -20}, {-100, 20}})));
    Modelica.Blocks.Interfaces.RealInput x_output "Output signal connector" annotation(
      Placement(transformation(origin = {-10, 0}, extent = {{100, -10}, {120, 10}}), iconTransformation(extent = {{100, -10}, {120, 10}})));
  equation
    u_input = u;
    x_output = x;
  end CraneModelBlock;

  block PIDControllerBlock
    extends Modelica.Blocks.Icons.Block;
    Modelica.Blocks.Interfaces.RealInput pid_in annotation(
      Placement(transformation(origin = {-40, 0}, extent = {{-84, -12}, {-60, 12}}), iconTransformation(extent = {{-140, -20}, {-100, 20}})));
    Modelica.Blocks.Interfaces.RealOutput pid_out annotation(
      Placement(transformation(extent = {{100, -10}, {120, 10}}), iconTransformation(extent = {{100, -10}, {120, 10}})));
    Modelica.Blocks.Math.Sum sum11(nin = 3) annotation(
      Placement(transformation(origin = {42, 0}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Gain gain(k = K_p) annotation(
      Placement(transformation(origin = {-10, 44}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Continuous.Integrator integrator(k = K_I) annotation(
      Placement(transformation(origin = {-12, 0}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Continuous.Derivative derivative(k = K_D) annotation(
      Placement(transformation(origin = {-10, -36}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Feedback feedback annotation(
      Placement(transformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}})));
  CraneModelBlock craneModelBlock annotation(
      Placement(transformation(origin = {80, 0}, extent = {{-10, -10}, {10, 10}})));
  equation
    connect(feedback.y, integrator.u) annotation(
      Line(points = {{-70, 0}, {-24, 0}}, color = {0, 0, 127}));
    connect(derivative.u, feedback.y) annotation(
      Line(points = {{-22, -36}, {-42, -36}, {-42, 0}, {-70, 0}}, color = {0, 0, 127}));
    connect(sum11.u, integrator.y) annotation(
      Line(points = {{30, 0}, {0, 0}}, color = {0, 0, 127}));
    connect(derivative.y, sum11.u) annotation(
      Line(points = {{2, -36}, {24, -36}, {24, 0}, {30, 0}}, color = {0, 0, 127}));
    connect(gain.y, sum11.u) annotation(
      Line(points = {{1, 44}, {24, 44}, {24, 0}, {30, 0}}, color = {0, 0, 127}));
    connect(gain.u, feedback.y) annotation(
      Line(points = {{-22, 44}, {-42, 44}, {-42, 0}, {-70, 0}}, color = {0, 0, 127}));
  connect(craneModelBlock.u_input, sum11.y) annotation(
      Line(points = {{68, 0}, {54, 0}}, color = {0, 0, 127}));
  connect(craneModelBlock.x_output, feedback.u2) annotation(
      Line(points = {{92, 0}, {94, 0}, {94, -72}, {-80, -72}, {-80, -8}}, color = {0, 0, 127}));
  connect(craneModelBlock.x_output, pid_out) annotation(
      Line(points = {{92, 0}, {110, 0}}, color = {0, 0, 127}));
  connect(pid_in, feedback.u1) annotation(
      Line(points = {{-112, 0}, {-88, 0}}, color = {0, 0, 127}));
  annotation(
      Diagram);
end PIDControllerBlock;

  model PIDControlLoopModel
  equation

  end PIDControlLoopModel;
  annotation(
    uses(Modelica(version = "4.0.0")));
end GantryControlSystem;
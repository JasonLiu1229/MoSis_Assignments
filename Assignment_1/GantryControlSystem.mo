package GantryControlSystem
  model CraneModel
    type DampingFactor = Real(unit = "N/(m/s)");
    // Parameters
    parameter Modelica.Units.SI.Mass m = 0.2 "The mass of the pendulum bob/container";
    parameter Modelica.Units.SI.Mass M = 10 "The mass of the trolley/cart";
    parameter Modelica.Units.SI.Length r = 1 "The length of the rope connecting the trolley/cart and the pendulum bob/container";
    parameter DampingFactor d_p = 0.12 "The damping factor of the pendulum";
    parameter DampingFactor d_c = 4.7895 "The damping factor for the motion of the trolley/cart";
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
    Modelica.Blocks.Interfaces.RealInput pid_in annotation(
      Placement(transformation(origin = {-40, 60}, extent = {{-84, -12}, {-60, 12}}), iconTransformation(origin = {0, 60}, extent = {{-140, -20}, {-100, 20}})));
    Modelica.Blocks.Interfaces.RealInput feedback_in annotation(
      Placement(transformation(origin = {-40, -60}, extent = {{-84, -12}, {-60, 12}}), iconTransformation(origin = {0, -60}, extent = {{-140, -20}, {-100, 20}})));
    Modelica.Blocks.Interfaces.RealOutput pid_out annotation(
      Placement(transformation(extent = {{100, -10}, {120, 10}}), iconTransformation(extent = {{100, -10}, {120, 10}})));
    Modelica.Blocks.Math.MultiSum suma11(nu = 3)  annotation(
      Placement(transformation(origin = {60, 0}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Gain gain(k = K_p) annotation(
      Placement(transformation(origin = {-10, 44}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Continuous.Integrator integrator(k = K_i) annotation(
      Placement(transformation(origin = {-12, 0}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Continuous.Derivative derivative(k = K_d) annotation(
      Placement(transformation(origin = {-10, -36}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Feedback feedback annotation(
      Placement(transformation(origin = {-72, 0}, extent = {{-10, -10}, {10, 10}})));
    
    parameter Real K_p = 26 "The proportional gain of the PID controller";
    parameter Real K_i = 0 "The integral gain of the PID controller";
    parameter Real K_d = 10 "The derivative gain of the PID controller";
  
  equation
    connect(feedback.y, integrator.u) annotation(
      Line(points = {{-63, 0}, {-24, 0}}, color = {0, 0, 127}));
    connect(derivative.u, feedback.y) annotation(
      Line(points = {{-22, -36}, {-42, -36}, {-42, 0}, {-63, 0}}, color = {0, 0, 127}));
    connect(gain.u, feedback.y) annotation(
      Line(points = {{-22, 44}, {-42, 44}, {-42, 0}, {-63, 0}}, color = {0, 0, 127}));
    connect(suma11.y, pid_out) annotation(
        Line(points = {{71, 0}, {110, 0}}, color = {0, 0, 127}));
    connect(feedback_in, feedback.u2) annotation(
        Line(points = {{-112, -60}, {-72, -60}, {-72, -8}}, color = {0, 0, 127}));
    connect(feedback.u1, pid_in) annotation(
        Line(points = {{-80, 0}, {-88, 0}, {-88, 60}, {-112, 60}}, color = {0, 0, 127}));
    connect(gain.y, suma11.u[1]) annotation(
        Line(points = {{2, 44}, {20, 44}, {20, 0}, {50, 0}}, color = {0, 0, 127}));
    connect(integrator.y, suma11.u[2]) annotation(
        Line(points = {{0, 0}, {50, 0}}, color = {0, 0, 127}));
    connect(derivative.y, suma11.u[3]) annotation(
        Line(points = {{2, -36}, {20, -36}, {20, 0}, {50, 0}}, color = {0, 0, 127}));
      annotation(
      Diagram);
  end PIDControllerBlock;

  model PIDControlLoopModel
  CraneModelBlock craneModelBlock annotation(
      Placement(transformation(origin = {44, 0}, extent = {{-10, -10}, {10, 10}})));
  PIDControllerBlock pIDControllerBlock annotation(
      Placement(transformation(origin = {-18, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Sources.Constant const(k = K_constant)  annotation(
      Placement(transformation(origin = {-76, 6}, extent = {{-10, -10}, {10, 10}})));
      
  parameter Real K_constant = 20 "The constant value for the constant block";
   
  equation
  connect(pIDControllerBlock.pid_out, craneModelBlock.u_input) annotation(
      Line(points = {{-6, 0}, {32, 0}}, color = {0, 0, 127}));
  connect(craneModelBlock.x_output, pIDControllerBlock.feedback_in) annotation(
      Line(points = {{56, 0}, {74, 0}, {74, -52}, {-56, -52}, {-56, -6}, {-30, -6}}, color = {0, 0, 127}));
  connect(pIDControllerBlock.pid_in, const.y) annotation(
      Line(points = {{-30, 6}, {-64, 6}}, color = {0, 0, 127}));
  end PIDControlLoopModel;
  annotation(
    uses(Modelica(version = "4.0.0")));
end GantryControlSystem;
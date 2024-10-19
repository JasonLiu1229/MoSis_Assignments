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
    theta = 30*Modelica.Constants.pi/180;
    omega = 0;
  equation
    der(theta) = omega;
    der(omega) = -((d_p*omega) + (m*g*r*sin(theta)))/(m*(r)^2);
// u signal change
    if time < 0.5 then
      u = 1000;
    else
      u = 0;
    end if;
  end CraneModelExpTwo;

  block CraneModelBlock
    extends GantryControlSystem.CraneModel;
    extends Modelica.Blocks.Icons.Block;
    Modelica.Blocks.Interfaces.RealInput u_input "Input signal connector";
    Modelica.Blocks.Interfaces.RealInput x_output "Output signal connector";
  equation
    u_input = u;
    x_output = x;
  end CraneModelBlock;

  block PIDControllerBlock
    extends Modelica.Blocks.Icons.Block;
    
    Modelica.Blocks.Interfaces.RealInput pid_in;
    Modelica.Blocks.Interfaces.RealOutput pid_out;
    Modelica.Blocks.Math.Sum sum11(nin = 3) annotation(
      Placement(transformation(origin = {72, 18}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Gain gain(k = K_p)  annotation(
        Placement(transformation(origin = {-12, 80}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Gain gain1(k = K_I) annotation(
        Placement(transformation(origin = {-10, 38}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Math.Gain gain11(k = K_D) annotation(
        Placement(transformation(origin = {-10, -68}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Integrator integrator annotation(
      Placement(transformation(origin = {-12, 0}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Continuous.Derivative derivative annotation(
      Placement(transformation(origin = {-10, -36}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product product annotation(
      Placement(transformation(origin = {26, 18}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product product1 annotation(
      Placement(transformation(origin = {24, -42}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Product product2 annotation(
      Placement(transformation(origin = {24, 60}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Blocks.Math.Feedback feedback annotation(
      Placement(transformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}})));
    equation
    connect(product.y, sum11.u) annotation(
      Line(points = {{37, 18}, {60, 18}}, color = {0, 0, 127}));
    connect(integrator.y, product.u2) annotation(
      Line(points = {{-1, 0}, {6, 0}, {6, 12}, {14, 12}}, color = {0, 0, 127}));
    connect(product.u1, gain1.y) annotation(
      Line(points = {{14, 24}, {6, 24}, {6, 38}, {2, 38}}, color = {0, 0, 127}));
    connect(derivative.y, product1.u1) annotation(
      Line(points = {{1, -36}, {12, -36}}, color = {0, 0, 127}));
    connect(product1.u2, gain11.y) annotation(
      Line(points = {{12, -48}, {12, -68}, {2, -68}}, color = {0, 0, 127}));
    connect(gain.y, product2.u1) annotation(
      Line(points = {{0, 80}, {0, 66}, {12, 66}}, color = {0, 0, 127}));
  connect(sum11.y, feedback.u2) annotation(
      Line(points = {{84, 18}, {90, 18}, {90, -90}, {-80, -90}, {-80, -8}}, color = {0, 0, 127}));
  connect(feedback.y, integrator.u) annotation(
      Line(points = {{-70, 0}, {-24, 0}}, color = {0, 0, 127}));
  connect(derivative.u, feedback.y) annotation(
      Line(points = {{-22, -36}, {-42, -36}, {-42, 0}, {-70, 0}}, color = {0, 0, 127}));
  connect(product2.u2, feedback.y) annotation(
      Line(points = {{12, 54}, {-42, 54}, {-42, 0}, {-70, 0}}, color = {0, 0, 127}));
  connect(product1.y, sum11.u) annotation(
      Line(points = {{36, -42}, {46, -42}, {46, 18}, {60, 18}}, color = {0, 0, 127}));
  connect(product2.y, sum11.u) annotation(
      Line(points = {{36, 60}, {46, 60}, {46, 18}, {60, 18}}, color = {0, 0, 127}));
  end PIDControllerBlock;

  model PIDControlLoopModel
  equation

  end PIDControlLoopModel;
  annotation(
    uses(Modelica(version = "4.0.0")));
end GantryControlSystem;
using UnityEngine;

public class motorscript : MonoBehaviour
{
    [Header("Motor Positions")]
    public Transform motorLeft;
    public Transform motorRight;

    [Header("Motor Settings")]
    public float maxThrust = 10f;
    public float steeringStrength = 0.7f;

    private Rigidbody rb;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        // W/S = forward/reverse
        float throttle = 0f;

        if (Input.GetKey(KeyCode.W))
            throttle = 1f;

        if (Input.GetKey(KeyCode.S))
            throttle = -1f;

        // A/D = steering
        float steering = 0f;

        if (Input.GetKey(KeyCode.A))
            steering = -1f;

        if (Input.GetKey(KeyCode.D))
            steering = 1f;

        // Differential thrust
        float leftThrust =
            throttle + steering * steeringStrength;

        float rightThrust =
            throttle - steering * steeringStrength;

        leftThrust = Mathf.Clamp(leftThrust, -1f, 1f);
        rightThrust = Mathf.Clamp(rightThrust, -1f, 1f);

        ApplyMotorForce(motorLeft, leftThrust);
        ApplyMotorForce(motorRight, rightThrust);
    }

    void ApplyMotorForce(Transform motor, float input)
    {
        if (motor == null)
            return;

        Vector3 force =
            transform.forward * input * maxThrust;

        rb.AddForceAtPosition(
            force,
            motor.position,
            ForceMode.Force
        );
    }
}

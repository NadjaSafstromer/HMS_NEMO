using UnityEngine;

public class Boatboyancy : MonoBehaviour
{

    public Transform[] boyancypoints;

    public float waterLevel = 0f;
    public float boyancyForce = 15f;
    public float waterDamp = 2f;
    public float waveAmplitude = 0.1f;
    public float waveFrequency = 0.25f;
    public float waveSpeed = 1f;

    private Rigidbody rb;

    float GetWaterHeight(Vector3 position)
    {
        float wave = Mathf.Sin(position.x * waveFrequency + Time.time * waveSpeed);

        return waterLevel + wave * waveAmplitude;
    }

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        foreach (Transform point in boyancypoints)
        {
            float waterHeight = GetWaterHeight(point.position);
            


            if (point.position.y < waterHeight)
            {
                float depth = waterHeight - point.position.y;

                Vector3 force = Vector3.up * depth * boyancyForce;

                rb.AddForceAtPosition(force, point.position);

                Vector3 dampingForce = rb.GetPointVelocity(point.position) * waterDamp;

                rb.AddForceAtPosition(dampingForce, point.position);
            }
        }
        
    }
}

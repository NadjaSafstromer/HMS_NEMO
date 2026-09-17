using UnityEngine;
using UnityEngine.Rendering.HighDefinition;

public class Buoyancy : MonoBehaviour
{
    [Header("HDRP Water")]
    public WaterSurface waterSurface;

    [Header("Buoyancy Points")]
    public Transform[] buoyancyPoints;

    [Header("Buoyancy Settings")]
    public float buoyancyForce = 25f;
    public float waterDamping = 3f;
    public float maxDepth = 0.20f;

    private Rigidbody rb;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void FixedUpdate()
    {
        if (waterSurface == null || rb == null)
            return;

        foreach (Transform point in buoyancyPoints)
        {
            if (point == null)
                continue;

            WaterSearchParameters searchParameters =
                new WaterSearchParameters();

            searchParameters.startPositionWS = point.position;
            searchParameters.targetPositionWS = point.position;
            searchParameters.error = 0.01f;
            searchParameters.maxIterations = 8;
            searchParameters.includeDeformation = true;
            searchParameters.excludeSimulation = false;

            WaterSearchResult searchResult;

            if (waterSurface.ProjectPointOnWaterSurface(
                    searchParameters,
                    out searchResult))
            {
                Debug.Log("POINT: " + point.name + " | Point Y: " + point.position.y +" | Water Y: " + searchResult.projectedPositionWS.y);

                float waterHeight =
                    searchResult.projectedPositionWS.y;

                float depth = waterHeight - point.position.y;

                if (depth > 0f)
                {
                    // Prevent extremely large forces if a point
                    // becomes deeply submerged.
                    depth = Mathf.Min(depth, maxDepth);

                    // Upward buoyancy force.
                    Vector3 force =
                        Vector3.up * buoyancyForce * depth;

                    rb.AddForceAtPosition(
                        force,
                        point.position,
                        ForceMode.Force);

                    // Damping at this specific point.
                    Vector3 pointVelocity =
                        rb.GetPointVelocity(point.position);

                    Vector3 dampingForce =
                        -pointVelocity * waterDamping * depth;

                    rb.AddForceAtPosition(
                        dampingForce,
                        point.position,
                        ForceMode.Force);
                }
            }
        }
    }
}
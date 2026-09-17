using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;

    public Vector3 offset = new Vector3(0f, 1.5f, -2.5f);
    public float smoothSpeed = 5f;

    void LateUpdate()
    {
        if (target == null)
            return;

        // Offset follows the boat's orientation
        Vector3 desiredPosition =
            target.position + target.rotation * offset;

        transform.position = Vector3.Lerp(
            transform.position,
            desiredPosition,
            smoothSpeed * Time.deltaTime
        );

        // Camera looks toward the boat
        Vector3 lookDirection = target.position - transform.position;

        if (lookDirection != Vector3.zero)
        {
            Quaternion desiredRotation =
                Quaternion.LookRotation(lookDirection);

            transform.rotation = Quaternion.Slerp(
                transform.rotation,
                desiredRotation,
                smoothSpeed * Time.deltaTime
            );
        }
    }
}
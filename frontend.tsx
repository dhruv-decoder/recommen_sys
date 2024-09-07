const fetchRecommendations = async (studentId: string) => {
  const response = await fetch('/get-recommendations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ student_id: studentId }),
  });
  const data = await response.json();
  console.log(data.recommended_alumni);
};

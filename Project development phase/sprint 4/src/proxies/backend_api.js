import { BASE_URL } from "../utils/helper";

export const loginUser = async (inputs) => {
  try {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      body: JSON.stringify(inputs),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
};

export const registerUser = async (inputs) => {
  try {
    const response = await fetch(`${BASE_URL}/auth/signup`, {
      method: "POST",
      body: JSON.stringify(inputs),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
};

export const getUserSkills = async (token) => {
  try {
    const response = await fetch(`${BASE_URL}/user/skills`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (response.ok) {
      const { skills } = await response.json();
      return skills;
    } else {
      return null;
    }
  } catch (error) {
    console.error(error);
  }
};

export const saveUserSkills = async (skills, token) => {
  try {
    const response = await fetch(`${BASE_URL}/user/skills`, {
      method: "POST",
      body: JSON.stringify({ skills }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (response.ok) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
  }
};

export const removeUserSkills = async (skills, token) => {
  try {
    const response = await fetch(`${BASE_URL}/user/skills`, {
      method: "DELETE",
      body: JSON.stringify({ skills }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (response.ok) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
  }
};

export const updateUserDetails = async (inputs, token) => {
  try {
    const response = await fetch(`${BASE_URL}/user/profile`, {
      method: "POST",
      body: JSON.stringify(inputs),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      return null;
    }
  } catch (error) {
    console.error(error);
  }
};

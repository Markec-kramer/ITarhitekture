const usersService = require("../services/usersService");

const getAllUsers = async (req, res) => {
  try {
    console.info("Fetching all users");
    const users = await usersService.getAllUsers();
    res.status(200).json(users);
  } catch (error) {
    console.error("Failed to fetch users", error);
    res.status(500).json({ error: "Failed to fetch users" });
  }
};

const getUserById = async (req, res) => {
  try {
    console.info(`Fetching user with id: ${req.params.id}`);
    const user = await usersService.getUserById(req.params.id);

    if (!user) {
      console.warn(`User not found with id: ${req.params.id}`);
      return res.status(404).json({ error: "User not found" });
    }

    res.status(200).json(user);
  } catch (error) {
    console.error(`Failed to fetch user with id: ${req.params.id}`, error);
    res.status(500).json({ error: "Failed to fetch user" });
  }
};

const createUser = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    if (!name || !email || !password) {
      console.warn("Validation failed: name, email and password are required");
      return res.status(400).json({ error: "Name, email and password are required" });
    }

    console.info(`Creating user with email: ${email}`);

    const newUser = await usersService.createUser({
      name,
      email,
      password,
    });

    res.status(201).json(newUser);
  } catch (error) {
    console.error("Failed to create user", error);

    if (error.code === "P2002") {
      return res.status(409).json({ error: "Email already exists" });
    }

    res.status(500).json({ error: "Failed to create user" });
  }
};

const updateUser = async (req, res) => {
  try {
    console.info(`Updating user with id: ${req.params.id}`);
    const updatedUser = await usersService.updateUser(req.params.id, req.body);
    res.status(200).json(updatedUser);
  } catch (error) {
    console.error(`Failed to update user with id: ${req.params.id}`, error);
    res.status(500).json({ error: "Failed to update user" });
  }
};

const deleteUser = async (req, res) => {
  try {
    console.info(`Deleting user with id: ${req.params.id}`);
    await usersService.deleteUser(req.params.id);
    res.status(204).send();
  } catch (error) {
    console.error(`Failed to delete user with id: ${req.params.id}`, error);
    res.status(500).json({ error: "Failed to delete user" });
  }
};

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
};
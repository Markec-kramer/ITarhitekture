const usersRepository = require("../repositories/usersRepository");

const getAllUsers = async () => {
  return usersRepository.getAllUsers();
};

const getUserById = async (id) => {
  return usersRepository.getUserById(id);
};

const createUser = async (userData) => {
  return usersRepository.createUser(userData);
};

const updateUser = async (id, userData) => {
  return usersRepository.updateUser(id, userData);
};

const deleteUser = async (id) => {
  return usersRepository.deleteUser(id);
};

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
};
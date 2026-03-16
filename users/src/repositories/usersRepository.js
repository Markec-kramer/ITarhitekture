const prisma = require("../config/prismaClient");

const getAllUsers = async () => {
  return prisma.user.findMany();
};

const getUserById = async (id) => {
  return prisma.user.findUnique({
    where: { id: Number(id) },
  });
};

const createUser = async (userData) => {
  return prisma.user.create({
    data: userData,
  });
};

const updateUser = async (id, userData) => {
  return prisma.user.update({
    where: { id: Number(id) },
    data: userData,
  });
};

const deleteUser = async (id) => {
  return prisma.user.delete({
    where: { id: Number(id) },
  });
};

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
};
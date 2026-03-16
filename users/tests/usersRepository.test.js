const prisma = require("../src/config/prismaClient");
const usersRepository = require("../src/repositories/usersRepository");

beforeAll(async () => {
  await prisma.user.deleteMany();
});

afterEach(async () => {
  await prisma.user.deleteMany();
});

afterAll(async () => {
  await prisma.$disconnect();
});

describe("Users repository", () => {
  test("should create a user", async () => {
    const user = await usersRepository.createUser({
      name: "Repository User",
      email: "repo@example.com",
      password: "test123",
    });

    expect(user.id).toBeDefined();
    expect(user.email).toBe("repo@example.com");
  });

  test("should get all users", async () => {
    await usersRepository.createUser({
      name: "User One",
      email: "one@example.com",
      password: "test123",
    });

    const users = await usersRepository.getAllUsers();

    expect(users.length).toBe(1);
    expect(users[0].email).toBe("one@example.com");
  });

  test("should get user by id", async () => {
    const createdUser = await usersRepository.createUser({
      name: "User Two",
      email: "two@example.com",
      password: "test123",
    });

    const user = await usersRepository.getUserById(createdUser.id);

    expect(user).not.toBeNull();
    expect(user.email).toBe("two@example.com");
  });

  test("should update user", async () => {
    const createdUser = await usersRepository.createUser({
      name: "User Three",
      email: "three@example.com",
      password: "test123",
    });

    const updatedUser = await usersRepository.updateUser(createdUser.id, {
      name: "Updated User Three",
    });

    expect(updatedUser.name).toBe("Updated User Three");
  });

  test("should delete user", async () => {
    const createdUser = await usersRepository.createUser({
      name: "User Four",
      email: "four@example.com",
      password: "test123",
    });

    await usersRepository.deleteUser(createdUser.id);

    const user = await usersRepository.getUserById(createdUser.id);
    expect(user).toBeNull();
  });
});
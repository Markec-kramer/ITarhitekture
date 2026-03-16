const request = require("supertest");
const app = require("../src/app");
const prisma = require("../src/config/prismaClient");

beforeAll(async () => {
  await prisma.user.deleteMany();
});

afterEach(async () => {
  await prisma.user.deleteMany();
});

afterAll(async () => {
  await prisma.$disconnect();
});

describe("Users API endpoints", () => {
  test("GET /api/users should return empty array", async () => {
    const response = await request(app).get("/api/users");

    expect(response.statusCode).toBe(200);
    expect(response.body).toEqual([]);
  });

  test("POST /api/users should create a new user", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({
        name: "Janez Novak",
        email: "janez@example.com",
        password: "test123",
      });

    expect(response.statusCode).toBe(201);
    expect(response.body.name).toBe("Janez Novak");
    expect(response.body.email).toBe("janez@example.com");
  });

  test("GET /api/users/:id should return user by id", async () => {
    const createdUser = await prisma.user.create({
      data: {
        name: "Ana Novak",
        email: "ana@example.com",
        password: "test123",
      },
    });

    const response = await request(app).get(`/api/users/${createdUser.id}`);

    expect(response.statusCode).toBe(200);
    expect(response.body.id).toBe(createdUser.id);
    expect(response.body.email).toBe("ana@example.com");
  });

  test("PUT /api/users/:id should update user", async () => {
    const createdUser = await prisma.user.create({
      data: {
        name: "Marko",
        email: "marko@example.com",
        password: "test123",
      },
    });

    const response = await request(app)
      .put(`/api/users/${createdUser.id}`)
      .send({
        name: "Marko Updated",
      });

    expect(response.statusCode).toBe(200);
    expect(response.body.name).toBe("Marko Updated");
  });

  test("DELETE /api/users/:id should delete user", async () => {
    const createdUser = await prisma.user.create({
      data: {
        name: "Delete Me",
        email: "delete@example.com",
        password: "test123",
      },
    });

    const response = await request(app).delete(`/api/users/${createdUser.id}`);

    expect(response.statusCode).toBe(204);

    const deletedUser = await prisma.user.findUnique({
      where: { id: createdUser.id },
    });

    expect(deletedUser).toBeNull();
  });
});
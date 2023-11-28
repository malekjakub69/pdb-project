const chai = require('chai');
const chaiHttp = require('chai-http');
const expect = chai.expect;

chai.use(chaiHttp);

const apiUrl = "http://localhost:5123/api/mysql"; // replace with your API url

describe("API Tests", function () {
    it("should get all users", function (done) {
        chai.request(apiUrl)
            .get('/users')
            .end(function (err, res) {
                expect(res).to.have.status(200);
                expect(res.body.users).to.be.a('array');
                done();
            });
    });

    it("should get all articles", function (done) {
        chai.request(apiUrl)
            .get('/articles')
            .end(function (err, res) {
                expect(res).to.have.status(200);
                expect(res.body.articles).to.be.a('array');
                done();
            });
    });

    it("should create, not duplicate, and delete a user", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                // Try to create the same user
                chai.request(apiUrl)
                    .post('/user')
                    .send(testUser)
                    .end(function (err, res) {
                        expect(res).to.have.status(400); // assuming your API returns 409 for duplicate users

                        // Delete the user
                        chai.request(apiUrl)
                            .delete(`/user/${createdUserId}`)
                            .end(function (err, res) {
                                expect(res).to.have.status(200);

                                done();
                            });
                    });
            });
    });

    it("should create a user, create an article with that user as author, and delete the article", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                const testArticle = { title: "Test Article", content: "Test Content", perex: "perex", author_id: createdUserId };

                // Create a new article
                chai.request(apiUrl)
                    .post('/article')
                    .send(testArticle)
                    .end(function (err, res) {
                        expect(res).to.have.status(201);
                        expect(res.body).to.be.a('object');
                        const createdArticleId = res.body.article.id;

                        // Delete the article
                        chai.request(apiUrl)
                            .delete(`/article/${createdArticleId}`)
                            .end(function (err, res) {
                                expect(res).to.have.status(200);

                                // Delete the user
                                chai.request(apiUrl)
                                    .delete(`/user/${createdUserId}`)
                                    .end(function (err, res) {
                                        expect(res).to.have.status(200);

                                        done();
                                    });
                            });
                    });
            });
    });


});
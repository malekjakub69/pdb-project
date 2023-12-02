const chai = require('chai');
const chaiHttp = require('chai-http');
const expect = chai.expect;

chai.use(chaiHttp);

const apiUrl = "http://localhost:5123/api"; // replace with your API url

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

describe("API Tests", function () {
    it("should get all users", function (done) {
        chai.request(apiUrl)
            .get('/users')
            .end(function (err, res) {
                expect(res).to.have.status(200);
                expect(res.body.data).to.be.a('array');
                done();
            });
    });

    it("should get all articles", function (done) {
        chai.request(apiUrl)
            .get('/articles')
            .end(function (err, res) {
                expect(res).to.have.status(200);
                expect(res.body.data).to.be.a('array');
                done();
            });
    });

    it("should create, not duplicate, and delete a user", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/mysql/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                // Try to create the same user
                chai.request(apiUrl)
                    .post('/mysql/user')
                    .send(testUser)
                    .end(function (err, res) {
                        expect(res).to.have.status(400);

                        // Delete the user
                        chai.request(apiUrl)
                            .delete(`/mysql/user/${createdUserId}`)
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
            .post('/mysql/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                const testArticle = { title: "Test Article", content: "Test Content", perex: "perex", author_id: createdUserId };

                // Create a new article
                chai.request(apiUrl)
                    .post('/mysql/article')
                    .send(testArticle)
                    .end(function (err, res) {
                        expect(res).to.have.status(201);
                        expect(res.body).to.be.a('object');
                        const createdArticleId = res.body.article.id;

                        // Delete the article
                        chai.request(apiUrl)
                            .delete(`/mysql/article/${createdArticleId}`)
                            .end(function (err, res) {
                                expect(res).to.have.status(200);

                                // Delete the user
                                chai.request(apiUrl)
                                    .delete(`/mysql/user/${createdUserId}`)
                                    .end(function (err, res) {
                                        expect(res).to.have.status(200);

                                        done();
                                    });
                            });
                    });
            });
    });

    it("should create an article with comments", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/mysql/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                const testArticle = { title: "Test Article", content: "Test Content", perex: "perex", author_id: createdUserId };

                // Create a new article
                chai.request(apiUrl)
                    .post('/mysql/article')
                    .send(testArticle)
                    .end(function (err, res) {
                        expect(res).to.have.status(201);
                        expect(res.body).to.be.a('object');
                        const createdArticleId = res.body.article.id;

                        const comments = [
                            { comment: "Comment 1", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 2", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 3", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 4", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 5", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 6", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 7", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 8", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 9", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 10", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 11", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                        ];

                        // Add comments to the article
                        let commentCount = 0;
                        comments.forEach(comment => {
                            chai.request(apiUrl)
                                .post(`/mysql/comment`)
                                .send(comment)
                                .end(async function (err, res) {
                                    if (commentCount < 10) {
                                        expect(res).to.have.status(201);
                                        expect(res.body).to.be.a('object');
                                    } else {
                                        expect(res).to.have.status(500);
                                        expect(res.body).to.be.a('object');
                                    }
                                    await sleep(50);

                                    commentCount++;

                                    if (commentCount === comments.length) {
                                        // Delete the article
                                        chai.request(apiUrl)
                                            .delete(`/mysql/article/${createdArticleId}`)
                                            .end(function (err, res) {
                                                expect(res).to.have.status(200);

                                                // Delete the user
                                                chai.request(apiUrl)
                                                    .delete(`/mysql/user/${createdUserId}`)
                                                    .end(function (err, res) {
                                                        expect(res).to.have.status(200);

                                                        done();
                                                    });
                                            });
                                    }
                                });
                        });
                    });
            });
    });


    //TODO: to test



    it("should create user, articles with tags, assign likes and views, call /api/trends/<string:timeframe> and clean up", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/mysql/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                const testArticle = {
                    title: "Test Article", content: "Test Content", perex: "perex", author_id: createdUserId,
                    tags: ["tag1", "tag2", "tag3"]
                };

                // Create a new article
                chai.request(apiUrl)
                    .post('/mysql/article')
                    .send(testArticle)
                    .end(function (err, res) {
                        expect(res).to.have.status(201);
                        expect(res.body).to.be.a('object');
                        const createdArticleId = res.body.article.id;
                        // Assign likes and views to the article
                        chai.request(apiUrl)
                            .post(`/mysql/article/${createdArticleId}/likes`)
                            .send({ likes: 10 })
                            .end(function (err, res) {
                                expect(res).to.have.status(200);

                                chai.request(apiUrl)
                                    .post(`/mysql/article/${createdArticleId}/views`)
                                    .send({ views: 100 })
                                    .end(function (err, res) {
                                        expect(res).to.have.status(200);

                                        const timeframe = "week";

                                        // Call /api/trends/<string:timeframe>
                                        chai.request(apiUrl)
                                            .get(`/api/trends/${timeframe}`)
                                            .end(function (err, res) {
                                                expect(res).to.have.status(200);
                                                expect(res.body).to.be.a('object');

                                                // Clean up
                                                chai.request(apiUrl)
                                                    .delete(`/mysql/article/${createdArticleId}`)
                                                    .end(function (err, res) {
                                                        expect(res).to.have.status(200);

                                                        chai.request(apiUrl)
                                                            .delete(`/mysql/user/${createdUserId}`)
                                                            .end(function (err, res) {
                                                                expect(res).to.have.status(200);

                                                                done();
                                                            });
                                                    });
                                            });
                                    });
                            });
                    });
            });
    });


})
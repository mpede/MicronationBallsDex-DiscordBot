-- upgrade --
ALTER TABLE "newsarticle" ADD "color" BIGINT NOT NULL  DEFAULT 16744512;
-- downgrade --
ALTER TABLE "newsarticle" DROP COLUMN "color";

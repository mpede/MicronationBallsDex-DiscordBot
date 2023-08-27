-- upgrade --
ALTER TABLE "ball" ADD "tags" VARCHAR(400) NOT NULL;
ALTER TABLE "ball" ADD "location" VARCHAR(60) NOT NULL;
-- downgrade --
ALTER TABLE "ball" DROP COLUMN "tags";
ALTER TABLE "ball" DROP COLUMN "location";
